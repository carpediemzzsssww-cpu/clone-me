#!/usr/bin/env python3
"""Clone Me: inventory and normalize a twin's materials folder.

Stdlib only, Python 3.9+.

  python3 materials.py scan <materials_dir>
  python3 materials.py convert <kind> <input> [--me NAME_OR_EMAIL] [--out DIR] [--no-redact]

kinds: chatgpt, claude, telegram, whatsapp, chat-txt, mbox, x

Every converter keeps only the user's own words and writes Markdown to
<materials_dir>/_normalized/ (or --out). Phone numbers, emails and ID-like
numbers are redacted unless --no-redact.
"""
import argparse
import datetime as dt
import email
import email.header
import json
import mailbox
import os
import re
import sys
from email.utils import parseaddr

# ---------------------------------------------------------------- redaction

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
CN_ID_RE = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){15,18}\d(?!\d)")
PHONE_RE = re.compile(r"(?<![\d\w])(?:\+?\d{1,3}[ -]?)?(?:1[3-9]\d{9}|\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4})(?![\d\w])")


def redact(text, on=True):
    if not on or not text:
        return text
    text = EMAIL_RE.sub("[email]", text)
    text = CN_ID_RE.sub("[id]", text)
    text = CARD_RE.sub("[number]", text)
    text = PHONE_RE.sub("[phone]", text)
    return text


# ---------------------------------------------------------------- helpers

def ts(value):
    """Best-effort timestamp -> 'YYYY-MM-DD'."""
    if value is None or value == "":
        return ""
    try:
        if isinstance(value, (int, float)):
            return dt.datetime.utcfromtimestamp(float(value)).strftime("%Y-%m-%d")
        s = str(value)
        if s.isdigit():
            return dt.datetime.utcfromtimestamp(int(s)).strftime("%Y-%m-%d")
        return s[:10]
    except (ValueError, OverflowError, OSError):
        return ""


def write_md(out_dir, name, title, blocks, redact_on):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    total = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write("# %s\n\n" % title)
        f.write("> Only my own words. Converted %s by clone-me materials.py%s.\n\n"
                % (dt.date.today().isoformat(), "" if redact_on else " (no redaction)"))
        for heading, lines in blocks:
            lines = [redact(l.strip(), redact_on) for l in lines if l and l.strip()]
            if not lines:
                continue
            f.write("## %s\n\n" % heading)
            for l in lines:
                total += len(l)
                f.write(l.replace("\n", "  \n") + "\n\n")
    print("wrote %s  (%d sections, ~%d chars)" % (path, len(blocks), total))
    return path


def default_out(input_path):
    base = os.path.dirname(os.path.abspath(input_path))
    # Walk up to the materials/ folder if the export sits in a subfolder.
    probe = base
    for _ in range(4):
        if os.path.basename(probe) == "materials":
            return os.path.join(probe, "_normalized")
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    return os.path.join(base, "_normalized")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def require_me(args, kind):
    if not args.me:
        sys.exit("convert %s needs --me (your name as it appears in the export%s)"
                 % (kind, ", or your email" if kind == "mbox" else ""))
    return args.me


# ---------------------------------------------------------------- converters

def text_of_parts(parts):
    out = []
    for p in parts or []:
        if isinstance(p, str):
            out.append(p)
        elif isinstance(p, dict) and isinstance(p.get("text"), str):
            out.append(p["text"])
    return "\n".join(out).strip()


def conv_chatgpt(args):
    data = load_json(args.input)
    blocks = []
    for conv in data:
        msgs = []
        for node in (conv.get("mapping") or {}).values():
            m = node.get("message") or {}
            if (m.get("author") or {}).get("role") != "user":
                continue
            content = m.get("content") or {}
            text = text_of_parts(content.get("parts"))
            if text:
                msgs.append((m.get("create_time") or 0, text))
        msgs.sort(key=lambda x: x[0] or 0)
        if msgs:
            title = conv.get("title") or "untitled"
            blocks.append(("%s · %s" % (ts(conv.get("create_time")), title), [t for _, t in msgs]))
    blocks.sort(key=lambda b: b[0])
    return write_md(args.out, "chatgpt-me.md", "My ChatGPT prompts", blocks, args.redact)


def conv_claude(args):
    data = load_json(args.input)
    blocks = []
    for conv in data:
        lines = []
        for m in conv.get("chat_messages") or []:
            if m.get("sender") != "human":
                continue
            text = m.get("text") or text_of_parts(m.get("content"))
            if text:
                lines.append(text)
        if lines:
            blocks.append(("%s · %s" % (ts(conv.get("created_at")), conv.get("name") or "untitled"), lines))
    blocks.sort(key=lambda b: b[0])
    return write_md(args.out, "claude-me.md", "My Claude.ai prompts", blocks, args.redact)


def tg_text(t):
    if isinstance(t, str):
        return t
    if isinstance(t, list):
        return "".join(x if isinstance(x, str) else (x.get("text") or "") for x in t)
    return ""


def conv_telegram(args):
    data = load_json(args.input)
    my_id = None
    info = data.get("personal_information") or {}
    if info.get("user_id") is not None:
        my_id = "user%s" % info["user_id"]
    if my_id is None and not args.me:
        sys.exit("No personal_information in result.json: pass --me <your display name>")
    chats = (data.get("chats") or {}).get("list") or ([data] if "messages" in data else [])
    blocks = []
    for chat in chats:
        lines = []
        for m in chat.get("messages") or []:
            if m.get("type") != "message":
                continue
            mine = (my_id and m.get("from_id") == my_id) or (args.me and m.get("from") == args.me)
            if mine:
                text = tg_text(m.get("text"))
                if text.strip():
                    lines.append("%s  %s" % (ts(m.get("date")), text))
        if lines:
            blocks.append(("%s (%s)" % (chat.get("name") or "chat", chat.get("type") or ""), lines))
    return write_md(args.out, "telegram-me.md", "My Telegram messages", blocks, args.redact)


# "12/31/23, 9:15 PM - Name: text" | "[31/12/2023, 21:15:00] Name: text"
WA_RE = re.compile(r"^\[?(\d{1,4}[./-]\d{1,2}[./-]\d{1,4}),? (\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APap]\.?[Mm]\.?)?)\]?(?: -)? ([^:]{1,60}): (.*)$")


def conv_whatsapp(args):
    me = require_me(args, "whatsapp")
    lines, cur = [], None
    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            raw = raw.rstrip("\n").replace("‎", "")
            m = WA_RE.match(raw)
            if m:
                cur = None
                if m.group(3).strip() == me and "<Media omitted>" not in m.group(4):
                    cur = len(lines)
                    lines.append("%s  %s" % (m.group(1), m.group(4)))
            elif cur is not None and raw.strip():
                lines[cur] += "\n" + raw
    name = os.path.splitext(os.path.basename(args.input))[0]
    return write_md(args.out, "whatsapp-%s-me.md" % slug(name), "My WhatsApp messages", [(name, lines)], args.redact)


# Generic "Name: text" or "2026-01-02 10:00 Name: text" or WeChat-style "Name 2026-01-02 10:00:00\ntext"
CHAT_HEAD_RE = re.compile(r"^(?:(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}[ T]\d{1,2}:\d{2}(?::\d{2})?)\s+)?([^:：\n]{1,40})[:：]\s?(.*)$")
WX_HEAD_RE = re.compile(r"^(.{1,40}?)\s+(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)\s*$")


def conv_chat_txt(args):
    me = require_me(args, "chat-txt")
    lines, cur, speaker, fresh = [], None, None, False
    with open(args.input, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            raw = raw.rstrip("\n")
            wx = WX_HEAD_RE.match(raw)
            if wx:
                speaker = wx.group(1).strip()
                cur = None
                if speaker == me:
                    cur = len(lines)
                    lines.append(wx.group(2)[:10])
                    fresh = True
                continue
            if fresh and cur is not None and raw.strip():
                lines[cur] += "  " + raw
                fresh = False
                continue
            fresh = False
            m = CHAT_HEAD_RE.match(raw)
            if m and m.group(2).strip() and not m.group(2).strip().startswith("http"):
                speaker = m.group(2).strip()
                cur = None
                if speaker == me:
                    cur = len(lines)
                    lines.append(((m.group(1) or "")[:10] + " " + m.group(3)).strip())
                continue
            if cur is not None and raw.strip():
                lines[cur] = (lines[cur] + "\n" + raw).strip()
    lines = [l for l in lines if l.strip()]
    if not lines:
        print("warning: no lines from %r found. Check --me matches the name in the file exactly." % me)
    name = os.path.splitext(os.path.basename(args.input))[0]
    return write_md(args.out, "chat-%s-me.md" % slug(name), "My chat messages", [(name, lines)], args.redact)


def decode_header(h):
    if not h:
        return ""
    out = []
    for part, enc in email.header.decode_header(h):
        if isinstance(part, bytes):
            try:
                out.append(part.decode(enc or "utf-8", errors="replace"))
            except LookupError:
                out.append(part.decode("utf-8", errors="replace"))
        else:
            out.append(part)
    return "".join(out)


QUOTE_TAIL_RE = re.compile(
    r"(^On .{5,200}wrote:\s*$|^在 .{2,200}写道[:：]\s*$|^-{2,}\s*Original Message|^-{2,}\s*原始邮件|^From: .+$|^发件人[:：])",
    re.M)


def plain_body(msg):
    def decode(part):
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""
        charset = part.get_content_charset() or "utf-8"
        try:
            return payload.decode(charset, errors="replace")
        except LookupError:
            return payload.decode("utf-8", errors="replace")

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                body = decode(part)
                break
        if not body:
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    body = re.sub(r"<[^>]+>", " ", decode(part))
                    break
    else:
        body = decode(msg)
        if msg.get_content_type() == "text/html":
            body = re.sub(r"<[^>]+>", " ", body)
    m = QUOTE_TAIL_RE.search(body)
    if m:
        body = body[:m.start()]
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith(">"))
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def recipient_kind(addr):
    domain = addr.split("@")[-1].lower() if "@" in addr else ""
    if domain.endswith(".edu") or ".edu." in domain:
        return "edu"
    if domain in ("gmail.com", "qq.com", "163.com", "126.com", "outlook.com", "hotmail.com", "icloud.com", "foxmail.com", "yahoo.com"):
        return "personal"
    return "work/other" if domain else "unknown"


def conv_mbox(args):
    me = require_me(args, "mbox").lower()
    box = mailbox.mbox(args.input)
    blocks = []
    for msg in box:
        sender = parseaddr(decode_header(msg.get("From")))[1].lower()
        if me not in sender:
            continue
        body = plain_body(msg)
        if not body:
            continue
        to = parseaddr(decode_header(msg.get("To")))[1]
        subject = decode_header(msg.get("Subject")) or "(no subject)"
        date = msg.get("Date") or ""
        try:
            date = email.utils.parsedate_to_datetime(date).strftime("%Y-%m-%d")
        except (TypeError, ValueError, IndexError):
            date = date[:16]
        blocks.append(("%s · to: %s · %s" % (date, recipient_kind(to), subject), [body]))
    blocks.sort(key=lambda b: b[0], reverse=True)
    return write_md(args.out, "sent-mail.md", "My sent email", blocks, args.redact)


def conv_x(args):
    with open(args.input, "r", encoding="utf-8") as f:
        raw = f.read()
    raw = raw[raw.index("["):] if "[" in raw else "[]"
    data = json.loads(raw)
    lines = []
    for item in data:
        t = item.get("tweet") or item
        text = t.get("full_text") or t.get("text") or ""
        if not text or text.startswith("RT @"):
            continue
        created = t.get("created_at") or ""
        try:
            created = dt.datetime.strptime(created, "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        except ValueError:
            created = created[:10]
        kind = "reply" if t.get("in_reply_to_status_id_str") else "post"
        lines.append((created, "%s  [%s] %s" % (created, kind, text)))
    lines.sort(reverse=True)
    return write_md(args.out, "x-posts.md", "My posts on X", [("posts and replies", [l for _, l in lines])], args.redact)


def slug(s):
    s = re.sub(r"[^\w一-鿿-]+", "-", s).strip("-").lower()
    return s[:40] or "chat"


CONVERTERS = {
    "chatgpt": conv_chatgpt,
    "claude": conv_claude,
    "telegram": conv_telegram,
    "whatsapp": conv_whatsapp,
    "chat-txt": conv_chat_txt,
    "mbox": conv_mbox,
    "x": conv_x,
}

# ---------------------------------------------------------------- scan

SENSITIVE_NAMES = {
    "export.xml": "Apple Health export (🔴 opt-in: use sleep/activity aggregates only)",
    "chat.db": "iMessage database (🔴: own side only)",
    "history": "browser history (🔴)",
    "location history": "location history (🔴)",
    "timeline": "location timeline (🔴)",
}
TEXT_EXT = {".md", ".txt", ".markdown", ".org", ".csv", ".json", ".js", ".html", ".htm", ".mbox", ".eml", ".xml", ".srt", ".vtt"}
DOC_EXT = {".pdf", ".docx", ".doc", ".pages", ".pptx", ".key", ".rtf"}
MEDIA_EXT = {".m4a", ".mp3", ".wav", ".mp4", ".mov", ".jpg", ".jpeg", ".png", ".heic", ".webp"}


def sniff(path):
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1]
    for key, label in SENSITIVE_NAMES.items():
        if name == key or (key in name and ext in ("", ".db", ".sqlite", ".json")):
            return label, "🔴", None
    head = ""
    if ext in TEXT_EXT or ext == "":
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                head = f.read(4000)
        except OSError:
            pass
    if name == "conversations.json":
        if '"mapping"' in head:
            return "ChatGPT export", "🟡", "chatgpt"
        if '"chat_messages"' in head:
            return "Claude.ai export", "🟡", "claude"
        return "AI chat export (unknown flavor)", "🟡", None
    if name == "result.json" and '"messages"' in head:
        return "Telegram export", "🟡", "telegram"
    if name in ("tweets.js", "tweet.js") or "window.YTD.tweet" in head:
        return "X archive tweets", "🟢", "x"
    if ext == ".mbox" or head.startswith("From "):
        return "mailbox (mbox)", "🟡", "mbox"
    if ext == ".eml":
        return "single email", "🟡", None
    if ext == ".txt" and WA_RE.match(head.split("\n", 1)[0].replace("‎", "")):
        return "WhatsApp chat export", "🟡", "whatsapp"
    if ext == ".txt" and (WX_HEAD_RE.search(head.split("\n", 3)[0] if head else "") or CHAT_HEAD_RE.match(head.split("\n", 1)[0] if head else "")):
        return "chat log (txt)", "🟡", "chat-txt"
    if ext in (".md", ".markdown", ".org"):
        return "notes / writing", "🟡", None
    if ext == ".txt":
        return "text", "🟡", None
    if ext == ".csv":
        return "table (e.g. Goodreads / Letterboxd / 豆瓣 export)", "🟢", None
    if ext == ".json":
        return "JSON export", "🟡", None
    if ext in (".html", ".htm"):
        return "web page / export", "🟢", None
    if ext == ".ics":
        return "calendar", "🟡", None
    if ext == ".vcf":
        return "contacts (🔴 third-party data: names only)", "🔴", None
    if ext in DOC_EXT:
        return "document (read with a PDF/Office tool)", "🟢", None
    if ext in MEDIA_EXT:
        if ext in (".m4a", ".mp3", ".wav", ".mp4", ".mov"):
            return "audio/video (transcribe first)", "🟡", None
        return "image (read visually; screenshots of chats work)", "🟡", None
    return "unknown", "?", None


def count_pii(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read(2_000_000)
    except OSError:
        return 0, 0
    return len(text), len(EMAIL_RE.findall(text)) + len(PHONE_RE.findall(text)) + len(CN_ID_RE.findall(text))


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%d%s" % (n, unit)
        n //= 1024
    return "%dTB" % n


def scan(args):
    root = os.path.abspath(args.dir)
    if not os.path.isdir(root):
        sys.exit("not a folder: %s" % root)
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "_normalized"]
        for fn in filenames:
            if fn.startswith("."):
                continue
            p = os.path.join(dirpath, fn)
            label, level, conv = sniff(p)
            size = os.path.getsize(p)
            chars, pii = ("", "")
            ext = os.path.splitext(fn)[1].lower()
            if (ext in TEXT_EXT or ext == "") and size < 200_000_000 and level != "🔴":
                c, n = count_pii(p)
                chars, pii = ("~%d" % c if size <= 2_000_000 else "~%s+" % human(size)), n
            rows.append((os.path.relpath(p, root), label, level, human(size), chars, pii, conv))
    if not rows:
        print("Empty. Drop exports into %s and scan again." % root)
        return
    print("| file | looks like | level | size | chars | PII hits | next step |")
    print("|---|---|---|---|---|---|---|")
    for rel, label, level, size, chars, pii, conv in sorted(rows):
        step = ("`convert %s`" % conv) if conv else "read directly"
        print("| %s | %s | %s | %s | %s | %s | %s |" % (rel, label, level, size, chars, pii, step))
    norm = os.path.join(root, "_normalized")
    if os.path.isdir(norm):
        done = sorted(os.listdir(norm))
        print("\nAlready normalized: %s" % (", ".join(done) if done else "nothing"))


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="Clone Me materials helper")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("scan", help="inventory a materials folder")
    s.add_argument("dir")
    c = sub.add_parser("convert", help="normalize an export to my-words-only Markdown")
    c.add_argument("kind", choices=sorted(CONVERTERS))
    c.add_argument("input")
    c.add_argument("--me", help="your name as it appears in the export, or your email for mbox")
    c.add_argument("--out", help="output folder (default: materials/_normalized)")
    c.add_argument("--no-redact", dest="redact", action="store_false", help="keep emails/phones/IDs")
    args = ap.parse_args(argv)
    if args.cmd == "scan":
        scan(args)
    elif args.cmd == "convert":
        if not os.path.exists(args.input):
            sys.exit("not found: %s" % args.input)
        args.out = args.out or default_out(args.input)
        CONVERTERS[args.kind](args)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
