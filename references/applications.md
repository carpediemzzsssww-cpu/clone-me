# Applications: what the twin can do

Three families: **represent me** (others meet the twin or its drafts), **understand me** (the twin helps the user think), **beyond me** (time, other twins, new formats).

## Menu (for step 1 — show short labels)

| Key | 中文 | One line |
|---|---|---|
| `intro` | 介绍我 | the right self-intro for any audience and length |
| `outreach` | 替我联络 | cold emails / DMs to people I want to reach, in my voice |
| `inbox` | 收件箱分身 | triage mail and DMs, draft replies per relationship |
| `social` | 社媒分身 | posts from my rough notes, replies to comments, consistent persona |
| `site` | 网站分身 | a twin on my personal site that visitors can talk to |
| `career` | 求职分身 | tailored resume bullets, screening answers, mock interviews |
| `schedule` | 约时间 | propose times from my calendar, write the reply |
| `brain` | 第二大脑 | "what did I think about X last year?" with sources |
| `decide` | 决策镜子 | "what would I choose?" and "where am I contradicting myself?" |
| `weekly` | 周回顾 | weekly digest in my voice; refreshes now.md |
| `ai-base` | AI 底座 | make every AI tool I use know me (CLAUDE.md, ChatGPT…) |
| `capsule` | 时间胶囊 | yearly snapshots; talk to past me; what changed |
| `twin-talk` | 分身对谈 | my twin talks with a friend's twin (both consent) to find overlaps |
| `product` | 产品客服 | not me: a twin of my product, from its codebase / docs |

## Unlock table

Show after extraction and after every `feed`. ✓ unlocked · ◐ works but thin · ○ locked.

| Scenario | Needs | Unlock hint |
|---|---|---|
| intro | core + memory (public) | resume or about page |
| outreach | voice (formal) + memory + relationships | 50+ sent emails, or 5 cold messages you've written |
| inbox | voice (casual + formal) + relationships + boundaries | sent mail by audience type |
| social | voice (public) + taste + now | 20+ own posts |
| site | core + memory (public) + boundaries + handoff contact | public bio + 5 projects + contact |
| career | memory (projects with results) + voice (formal) + judgment | resume + 3 project write-ups |
| schedule | now + calendar access + relationships | calendar connector or .ics |
| brain | memory + notes corpus | notes folder / AI chat export |
| decide | judgment (8+ principles with cases) | AI chat export or decision notes |
| weekly | now + calendar / notes / commits access | any two live sources |
| ai-base | core + voice + judgment | any |
| capsule | one snapshot (two to compare) | `/clone-me snapshot` |
| twin-talk | public export from both people | a friend with a twin |

Say it as: "再给我 **你最近 50 封发出去的邮件**，就能解锁 **替我联络**。"

## Scenario adapters

Create `twin/scenarios/<key>.md` the first time a scenario runs: copy the steps below, then add what the user teaches you (preferences, corrections).

### intro — 介绍我
1. Ask: audience (HR / 导师 / 同行 / 网友 / 投资人 / 活动现场), length (one line / 30s / 2min / written bio), language, goal (be remembered / get a reply / get hired).
2. Pull from core + memory `[public]` (+ `[friends]` if the audience is a friend); choose the 2–3 facts most relevant to *that* audience.
3. Write in the user's voice for that register. Give 2 versions: safe and bolder.
4. Variants on request: 小红书简介 (≤100 chars), X/LinkedIn bio, email signature, 开场白 for a talk, self-intro for a group chat.

### outreach — 替我联络
1. Ask who and why (a 学长 at a company, a creator to collaborate with, a professor, a recruiter, a journalist).
2. Research the recipient from **public** sources only, with the user's OK (their site, posts, papers). Never compile private information about them.
3. Find the real overlap: the user's memory items that matter to this person. If there is none, say so.
4. Draft in the user's formal or casual voice per relationships.md: subject line, ≤150 words for cold email, one clear ask, easy to say yes to.
5. Show the draft. On the user's yes: with a mail connector, create a **draft** in their mailbox (don't send); otherwise give copy-ready text. For DMs, give text to paste.
6. Optional: a follow-up draft for 5–7 days later; log the outreach in `scenarios/outreach.md` (who, date, status) if the user wants a tracker.

### inbox — 收件箱分身
1. With a mail / chat connector, read unread or a chosen label (read-only).
2. Triage into: needs me · twin can draft · FYI · ignore. Explain each in one line.
3. Draft replies for the "twin can draft" pile per relationship type; show them as a list.
4. The user approves / edits each → create drafts. Never send, never archive or delete without a per-item yes.
5. Learn: when the user edits a draft, record what changed as a voice rule.

### social — 社媒分身
- **Post from rough notes**: the user dumps raw thoughts / photos → 2–3 post drafts in their public voice (title, body, tags for 小红书; thread for X). Check against the user's own writing-style rules if they have them.
- **Reply to comments / DMs**: the user pastes them (or a browser reads their own notifications) → reply drafts; flag anything that needs the real person.
- **Persona check**: read a draft the user wrote and say what feels off-voice.
- Never post, like, follow or DM by itself.

### site — 网站分身
1. Run `export public` (see `export.md`) and show it to the user.
2. Copy `templates/site-twin/` into the user's site; put the public prompt into `api/_prompt.js`; set env vars on their host (they paste their own key in the host's dashboard).
3. The twin opens with a disclosure line ("我是 X 的 AI 分身…"), suggests 3–4 starter questions from memory `[public]`, and hands off to the contact for anything personal, commitments or unknowns.
4. Test locally with 10 visitor questions + 5 red-line probes before the user deploys. Deploy only when the user says so.

### career — 求职分身
- Tailor resume bullets for a JD from memory (only true facts, numbers with their date).
- Draft answers to screening questions in the user's voice.
- Mock interview: the twin answers first, then the user answers, then compare — the gap shows what the user hasn't articulated yet.

### schedule — 约时间
Read calendar (read-only) → find 3 slots respecting the user's rhythm (from now.md / judgment: e.g. no meetings before 10) → reply draft in the right register → invite only on the user's yes.

### brain — 第二大脑
Answer from the user's own notes / AI history / memory, always with source pointers and dates; say "I have nothing on this" rather than guessing. Good prompts: "我去年怎么看 X？" "我做过哪些和 Y 有关的事？" "我反复在想什么？"

### decide — 决策镜子
1. The user describes a choice. 2. Apply judgment.md principles; say which ones fire and how. 3. Give "what past-me would pick" + confidence. 4. **Devil's twin**: the strongest case against, and any past statement this choice contradicts. The user decides; the twin never pretends to know better.

### weekly — 周回顾
Read the week's calendar, notes, commits, posts (whatever's connected) → a short digest in the user's voice: done / in progress / stuck / noticed. Propose `now.md` updates; apply on yes.

### ai-base — AI 底座
Run `export` for each AI tool the user uses (CLAUDE.md, AGENTS.md, ChatGPT custom instructions, Claude Project, 豆包/Kimi agent). This is often the most useful first job for people who use AI daily.

### capsule — 时间胶囊
`snapshot` yearly (or at big moments: graduation, new job). Offer: "talk to my 2025 self", "what changed in me", a letter from this year's twin to next year's.

### twin-talk — 分身对谈
Both people export their **public** twin; load both and let them talk on a topic (collaboration ideas, a debate, getting to know each other) for a few rounds; then summarize overlaps and open questions for the two humans. Both must consent; only public layers.

### product — 产品客服 (kept from v1)
Not a personal twin: read the project's codebase, PRD, README and docs; ask bot name, scope, fallback, placement; write a product-knowledge prompt; use `templates/site-twin/` (React apps: adapt the widget into a component that calls `/api/chat`; keep the key server-side).
