# Data sources: where a person's data lives and how to reach it

Use this to build the user's **access plan** (SKILL.md step 2). Pick 5–8 sources that serve their first job; don't offer all of this at once.

## Five ways in (cheapest first)

| Route | How | Who can use it | Permission |
|---|---|---|---|
| **A. Drop a file** | The user exports from the platform and drops the file in `materials/` | everyone, including people in a plain chat app | none beyond the platform's own export |
| **B. Read locally** | Claude Code / Codex reads files or local databases on this machine | CLI users | file access the user approves; some need macOS Full Disk Access (the user grants it in System Settings → Privacy & Security; never do it for them) |
| **C. Connector / MCP** | A connector already in the session (Gmail, Google Calendar, Drive, Notion, GitHub, Slack, Linear…) | Claude Code, Claude.ai, Codex with MCP | OAuth the user approves; ask for **read-only** where the connector offers it |
| **D. Browser on your own account** | A browser tool reads pages the user is already signed in to (their own profile, their own posts) | when a browser tool is available | the user's existing sign-in; read only the user's own pages; never sign in for them |
| **E. Own API token** | The user creates a token on the platform and puts it in their env (`export X_TOKEN=…`) | developers | the token's scopes; choose the narrowest; never write it into the pack |

Check which of C and D actually exist in this session before offering them. If a platform has no export and no API, say so and use D or manual copy.

Sensitivity: 🟢 low (public posts, own published writing) · 🟡 medium (private notes, own side of chats, calendar) · 🔴 high (health, money, precise location, IDs, intimate chats, browser history). 🔴 is opt-in only, extract aggregates not details, never export publicly.

## The map

Layers: C core · V voice · J judgment · M memory · R relationships · T taste · N now.

### Writing & notes: the richest voice and memory

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| Obsidian / Markdown folders | point at the vault folder | B | V J M N | 🟡 |
| Apple Notes | no file export; read with `osascript` (Notes → body HTML) after the user OKs it, or the user copies notes into `materials/` | B / A | V M N | 🟡 |
| Notion | Settings → Export → Markdown & CSV; or the Notion connector; or an integration token shared with chosen pages only | A / C / E | V M | 🟡 |
| 飞书 / 语雀 / Google Docs | export docs to .docx/.md; Drive connector for Google Docs | A / C | V M | 🟡 |
| Blog, newsletter, 公众号 articles | the site's export / RSS / copy the articles | A / D | V J M | 🟢 |
| Resume, portfolio, about page | drop the files / URL | A / D | C M | 🟢 |
| Thesis, essays, course papers | drop files | A | V J M | 🟢 |

### Your conversations with AI: the best mirror of how you think

Almost nobody uses this, and it's gold for judgment: what you ask, how you push back, what you keep caring about.

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| ChatGPT | Settings → Data controls → Export data → `conversations.json` (`materials.py convert chatgpt`) | A | J V M N | 🟡 |
| Claude.ai | Settings → Privacy → Export data → `conversations.json` (`convert claude`) | A | J V M N | 🟡 |
| Claude Code | `~/.claude/projects/*/*.jsonl` transcripts; `CLAUDE.md` and memory folders are already a hand-made twin | B | J M N | 🟡 |
| Codex | `~/.codex/sessions/`, `~/.codex/AGENTS.md` | B | J M N | 🟡 |
| Custom instructions you already wrote | copy from ChatGPT / Claude settings | A | C V | 🟢 |

Keep only the user's own turns plus one-line summaries of what the AI answered.

### Email: voice per audience, relationships

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| Gmail | Gmail connector (read Sent, last 1–2 years); or Google Takeout → Mail → `.mbox` (`convert mbox --me you@x.com`) | C / A | V R M | 🟡 |
| Outlook / Microsoft 365 | Outlook connector if present; or export .pst → convert to mbox with a tool the user trusts | C / A | V R M | 🟡 |
| Any IMAP mail (QQ, 163, school mail) | the client's "export to mbox", or forward chosen threads | A | V R | 🟡 |

**Sent mail is the gold**: it's the user's voice with a known recipient type (professor, recruiter, friend, client).

### Chats: casual voice, relationships

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| 微信 | No official export. Safe routes: multi-select messages → 合并转发 to 文件传输助手 / email, then copy; screenshots (read them as images). Third-party local decryption tools exist but break the user agreement: don't recommend them; if the user already has a txt/csv of their own chats, `convert chat-txt --me <name>` works | A | V R | 🟡/🔴 |
| iMessage (Mac) | `~/Library/Messages/chat.db` (SQLite); the terminal needs Full Disk Access, which only the user can grant | B | V R | 🔴 |
| Telegram | Desktop → Settings → Advanced → Export Telegram data → JSON → `result.json` (`convert telegram`) | A | V R | 🟡 |
| WhatsApp | chat → More → Export chat → without media → .txt (`convert whatsapp --me <name>`) | A | V R | 🟡 |
| Slack / Discord / 飞书 IM | Slack connector or workspace export; Discord Settings → Privacy → Request data | C / A | V R | 🟡 |

Keep **only the user's own lines**. Other people's messages give context (one-line summary at most) and are never quoted in the twin.

### Social media: public voice, taste, persona

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| 小红书 | no personal data export for ordinary accounts: a browser on the user's own profile (notes, titles, likes count), or copy own notes; 创作者中心 data pages if the account has them | D / A | V T C | 🟢 |
| 微博 / 即刻 / 豆瓣 / B站 / 知乎 | no good official export: browser on own profile, or copy own posts / 豆瓣 marks | D / A | V T J | 🟢 |
| X (Twitter) | Settings → Your account → Download an archive → `data/tweets.js` (`convert x`) | A | V J T | 🟢 |
| Instagram / Facebook / Threads | Accounts Center → Your information → Download your information → JSON | A | V T | 🟢 |
| LinkedIn | Settings → Data privacy → Get a copy of your data | A | C M | 🟢 |
| Reddit / YouTube | Reddit data request; Google Takeout → YouTube (comments, history) | A | V T | 🟡 |
| Own comments on other people's posts | browser on own activity page | D | V J | 🟢 |

### Work & building

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| GitHub | `gh` CLI or GitHub connector: own repos, READMEs, commit messages, issues, PR reviews | B / C / E | M V J | 🟢 |
| Figma / Linear / Jira | connectors if present; exports | C / A | M | 🟡 |
| Talks, slides, podcasts, videos you made | drop files; transcribe audio/video (Whisper or any transcription tool) | A | V M | 🟢 |
| Voice memos | transcribe → spoken voice is different from written voice; keep both | A | V N | 🟡 |

### Life, time and taste

| Source | How to get it | Route | Feeds | Level |
|---|---|---|---|---|
| Calendar | Google Calendar connector; or export .ics; macOS: `icalBuddy` (brew) after the user OKs Calendar access | C / A / B | N R M | 🟡 |
| Photos | macOS Photos library via `osxphotos` (time, place, albums, people labels; no need to read images); phone album metadata | B | M T | 🔴 for precise location, 🟡 aggregated by city/year |
| Google Maps Timeline | now stored on the phone: Maps app → Timeline → export | A | M | 🔴 |
| Music | Spotify: Account → Privacy → Download your data; Spotify Web API (top tracks) with own token; Apple Music via privacy.apple.com; 网易云: public playlists via browser | A / E / D | T | 🟢 |
| Books / films | Goodreads / Letterboxd export CSV; 豆瓣 marks via browser | A / D | T J | 🟢 |
| Saves & bookmarks | 小红书收藏, browser bookmarks, Pocket/Readwise exports | A / D | T N | 🟡 |
| Health | iPhone Health → profile → Export All Health Data → `export.xml` | A | N (sleep / activity rhythm only) | 🔴 opt-in |
| Browser history | Chrome/Safari history SQLite | B | T N | 🔴, rarely worth it |
| Apple / Google full data copy | privacy.apple.com, takeout.google.com | A | everything | mixed: let the user pick categories |

### Other people's view of you (the outside layer)

| Source | How | Feeds |
|---|---|---|
| Friends' descriptions | send 3 questions to 3–5 friends: "用三个词形容我 / 我最常说的话 / 我什么时候最像我" | C V |
| Recommendation letters, performance reviews, comments on your work | drop files | C J |
| Friends as blind-test judges | see `evals.md` | proof |

### Never collect
Passwords, bank/card numbers, ID documents, other people's private data, accounts you don't own, data behind someone else's sign-in, anything the user can't legally share.

## Building the access plan

For the first job, pick sources in this order: one big **voice** source (sent mail, own posts, long writing) → one **judgment** source (AI chat history, decision notes) → one **memory** source (resume / GitHub / portfolio) → whatever that job specifically needs (calendar for scheduling, contacts' context for outreach, public bio for the site twin).

Present it like this:

| # | Source | Route | Permission you'll give | Level | Unlocks |
|---|---|---|---|---|---|
| 1 | Gmail · Sent · 2 yrs | connector, read-only | Google OAuth | 🟡 | outreach, inbox |
| 2 | ChatGPT export | drop file | none | 🟡 | decide, brain |
| 3 | 小红书 own notes | browser on your profile | your sign-in, read only | 🟢 | social, intro |

Then: "勾你愿意给的。之后随时 `/clone-me feed` 加更多。"
