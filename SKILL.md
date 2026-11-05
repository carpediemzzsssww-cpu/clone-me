---
name: clone-me
description: Build a living digital twin of the user (mainly themselves) from their own data — notes, chats, emails, social posts, AI chat history, calendar, photos — not from a questionnaire. Maps which data sources and permissions to use, distills voice / judgment / memory / relationships / taste into a portable "twin pack", proves likeness with a blind test, and puts the twin to work (introducing them, drafting outreach emails and DMs, social replies, a personal-site twin, a second brain, exports to CLAUDE.md / AGENTS.md / ChatGPT / Claude Projects). Use for /clone-me, "数字分身", "数字替身", "AI 克隆我", "make an AI version of me".
argument-hint: "[new | feed | test | use <scenario> | export <target> | snapshot] [name]"
disable-model-invocation: true
---

# Clone Me — a digital twin that grows from your own data

A twin is not a persona card. A persona card says "I am witty". A twin can write the email you would write, to this person, about this thing, and you can't tell it apart in a blind test.

So this skill works **material-first**: the user's own data is the evidence, a short interview only fills gaps, and every claim the twin makes about the user traces back to a source.

Files in this skill (read them when the step says so, not all up front):

| File | Read it when |
|---|---|
| `references/data-sources.md` | planning which data to connect (step 2, `feed`) |
| `references/extraction.md` | turning materials into twin files (step 4) |
| `references/applications.md` | choosing / running a scenario, unlock table |
| `references/evals.md` | `test` and the mini test in step 6 |
| `references/safety.md` | before collecting anything; before any outbound scenario |
| `references/export.md` | `export` |
| `templates/twin/` | creating a new pack |
| `templates/site-twin/` | the personal-website twin |
| `scripts/materials.py` | scanning and converting exports (Python 3.9+, stdlib only) |

## Language

Match the user's language from their first message (Chinese → run everything in Chinese). Platform names stay as the user knows them (微信, 小红书, Gmail).

## Commands

| Command | What it does |
|---|---|
| `/clone-me` or `/clone-me new [name]` | Start a twin, or resume the one that exists |
| `/clone-me feed` | Add new materials, re-extract, report what new scenarios unlocked |
| `/clone-me test` | Blind test + red-line test; turns misses into rules |
| `/clone-me use <scenario>` | Put the twin to work (intro, outreach, inbox, social, site, brain, decide…) |
| `/clone-me export <target>` | Export to a Claude Code skill, CLAUDE.md / AGENTS.md, ChatGPT, Claude Project, 豆包/Kimi agent, website |
| `/clone-me snapshot` | Freeze this year's twin; compare with past snapshots |

With no argument: if a twin pack exists (see "Where the twin lives"), show its status card (layers filled, last feed date, last test score, unlocked scenarios) and suggest the next best step; otherwise run `new`.

## The twin model: 8 layers

| Layer | File | Question it answers | Best evidence |
|---|---|---|---|
| Core | `core.md` | Who am I, in one breath? | bio, resume, about pages |
| Voice | `voice.md` | How do I say things? | sent emails, own chat lines, posts, long writing |
| Judgment | `judgment.md` | What would I choose, and why? | past decisions with reasons, AI chat history, reviews, arguments |
| Memory | `memory.md` | What have I done / know / believe? | projects, notes, timeline, GitHub, photo metadata |
| Relationships | `relationships.md` | How do I talk to whom? | chat/email split by recipient type (no third-party content) |
| Taste | `taste.md` | What do I love and hate? | music, books, films, saves, design references |
| Now | `now.md` | What's on my mind this month? | calendar, recent notes, commits, posts |
| Boundaries | `boundaries.md` | What must the twin never do or say? | the user; defaults in `references/safety.md` |

Every item in memory / relationships / taste / now carries a **visibility tag**: `[public]`, `[friends]`, `[private]`. Public exports only ever include `[public]` items. When unsure, tag `[private]`.

Every rule in voice / judgment carries **evidence**: a short quote or a source pointer (`_normalized/sent-mail.md#L120`). No evidence → it's a hypothesis: mark it `(guess)` and confirm with the user.

## Where the twin lives

Ask once, default to `~/clone-me/<slug>/`. Avoid iCloud-synced Desktop/Documents, and never put it inside a repo that gets pushed.

```
~/clone-me/<slug>/
  materials/            ← the drop zone (raw; stays on this machine; never exported)
    _normalized/        ← converted, your-side-only, PII-redacted text
  twin/                 ← the distilled pack (copied from templates/twin/)
    core.md voice.md judgment.md memory.md relationships.md taste.md now.md boundaries.md
    sources.md          ← every source used + permission granted + date
    scenarios/          ← one adapter per unlocked scenario
    evals/              ← blind-test questions, sealed answers, scores
  exports/              ← generated outputs (skill, prompts, site)
  snapshots/            ← frozen copies of twin/ by date
  .gitignore            ← ignores materials/ and exports/private/
```

## `new`: the flow

Keep it a conversation, not a form. Each phase ends with something the user can see.

### 1. First job (1 question)
Ask what they want the twin to *do first*. Offer the menu from `references/applications.md` (short labels only). The first job decides which data to ask for first — don't ask for everything up front.

### 2. Access plan
Read `references/data-sources.md` and build a personal **access plan**: 5–8 sources that best serve the first job, each with *how to get it* (drop a file / read locally / connector / browser / own API token), *what permission it needs*, *sensitivity* (🟢🟡🔴) and *which layers it feeds*.

- Check what's actually available in this session first: connector / MCP tools (Gmail, Google Calendar, Drive, Notion, GitHub, Slack…), a browser tool, readable local files. Offer live routes first, export routes second.
- Show it as a table and let the user tick. Permissions are the user's to grant: tell them exactly where to click (e.g. macOS Full Disk Access for iMessage). Never change system or security settings yourself, never ask for passwords; tokens go in the user's own env, never into the pack.
- Log every accepted source in `twin/sources.md` with date and scope ("Gmail, read-only, Sent, last 2 years").

### 3. Collect
- **Exports / files** → the user drops them into `materials/`. Run `python3 <skill>/scripts/materials.py scan <pack>/materials` to inventory, then `convert` for known formats (ChatGPT / Claude.ai export, Telegram, WhatsApp, mbox, X archive, plain chat txt). It keeps only the user's own side and redacts phone numbers, emails and ID numbers.
- **Connectors** → read only what the plan says (e.g. last 300 sent emails), save a digest to `materials/_normalized/`, not raw dumps.
- **Local sources** (Obsidian vault, Apple Notes, Claude Code / Codex history, git repos) → read in place with the user's OK; copy excerpts only.
- **Little or no data?** Run the **gap interview**: 3 voice samples on the spot ("reply to this message the way you would"), 3 decisions ("a choice you made and why"), "what's on your mind lately?", and 3 strong opinions. This is the old questionnaire, kept as a fallback.

### 4. Extract
Follow `references/extraction.md`. Fill the files from `templates/twin/`. Go layer by layer and show a short preview of each (5–8 bullets with evidence): "像不像？哪条不对？" → fix → next. Voice and judgment first: they matter most.

### 5. Unlock card
Show the **scenario unlock table** (`references/applications.md`): ✓ unlocked / ◐ partly / ○ locked, with "add X to unlock". This is how the user is guided to bring more material: always "give X → the twin can do Y", never "please complete the form".

### 6. Mini test
Run a 5-question blind test (`references/evals.md`) right away. A first score, even a bad one, makes the twin feel real and gives a number to improve.

### 7. First job
Run the job from step 1 with `use`. End with the status card and the 1–2 most valuable next materials.

## `feed`
Scan `materials/` for files not yet in `sources.md`, convert, extract only the delta, show a diff ("voice +2 rules, memory +5 items, now.md refreshed"), re-check the unlock table, announce newly unlocked scenarios. Suggest refreshing `now.md` monthly and a full `feed` quarterly.

## `test`
Follow `references/evals.md`: sealed answers → twin answers blind → shuffled pairs → the user (or a friend) guesses → score → every miss becomes a dated rule in voice.md / judgment.md → red-line test. Keep scores in `evals/scores.md` so progress is visible.

## `use <scenario>`
Load only the layers the scenario needs plus its adapter in `twin/scenarios/` (create it from `references/applications.md` the first time). Rules for every scenario:
- **Draft, don't send.** Anything that reaches another person (email, DM, comment, post, invite) is shown to the user and goes out only after a clear yes, each time. With a mail connector, create a *draft* instead of sending.
- **Disclose when the twin talks to others itself** (site twin, auto-replies): "I'm X's AI twin". A draft the user approves and sends as themselves is their own message.
- **Never invent facts about the user.** No memory → say so or ask; a public twin hands off to the real person's contact.
- After each job, ask one quick feedback question and write the correction back into the twin. That is how it learns.

## `export <target>`
Follow `references/export.md`. Two tiers: **private** (full pack, for the user's own AI tools) and **public** (only `[public]` items + boundaries, for anything other people talk to). Always show the public export to the user before it goes anywhere.

## `snapshot`
Copy `twin/` to `snapshots/<YYYY-MM-DD>/`. If an older snapshot exists, write "what changed in me": new beliefs, dropped interests, voice shifts. Offer "talk to my past self" (load the old snapshot as the twin).

## Safety (always on)
Read `references/safety.md` before collecting anything. In short: a twin of yourself by default; someone else only with their consent; read-only and least privilege; raw materials stay local; other people's words are never distilled into the twin; health / finance / precise location / IDs are 🔴 and opt-in only; no realistic face or voice clone presented as the real person.

## Style
A curious interviewer, not a form. Name good material when you see it ("这段邮件很能看出你的语气"). Keep turns short. When a layer is thin, say so plainly and name the one source that would fix it.
