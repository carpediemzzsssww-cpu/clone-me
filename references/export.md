# Export: put the twin wherever the user already works

Two tiers:
- **Private**: all layers (minus 🔴 details), for the user's own AI tools. Output to `exports/private/` (git-ignored).
- **Public**: only `[public]` memory/taste/now, core, public voice, boundaries. Output to `exports/public/`. Show it to the user in full before it goes anywhere.

Keep exports **short and rule-like**; long dumps dilute the voice. Always include 4–6 exemplar passages; they do more than any adjective.

## Targets

### `skill` → a Claude Code / Codex skill that *is* the user
Write `exports/private/<slug>-twin/SKILL.md`:
```
---
name: <slug>-twin
description: <Name>'s voice, judgment and context. Use whenever writing anything in <Name>'s name (posts, emails, READMEs, intros, replies) or deciding something on their behalf.
---
```
Body: core (short) → voice rules + exemplars → judgment principles → pointers to `memory.md`, `relationships.md`, `taste.md`, `now.md` (copy them next to SKILL.md as `references/`) → boundaries. Tell the user how to install: copy the folder to `~/.claude/skills/` (Claude Code) or `~/.codex/skills/` (Codex). Install only on their yes.

### `claude-md` / `agents-md` → "about me" for every project
A ≤60-line block for `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`: who I am, how I work, how to talk to me, my voice in 5 rules, current focus. Show a diff and append only on the user's yes; never overwrite their existing file.

### `chatgpt` → custom instructions / a GPT
- Custom instructions: two boxes, about 1,500 characters each: "what should ChatGPT know about you" (core + now + judgment highlights) and "how should it respond" (voice rules).
- GPT: instructions (up to 8,000 characters) + upload twin files as knowledge.

### `claude-project` → a Claude.ai Project
Project instructions = the private prompt; upload `memory.md`, `taste.md`, `relationships.md` as project knowledge.

### `doubao` / `kimi` / any agent builder
One system prompt (the private or public tier, as the user chooses) + knowledge files if the platform supports them.

### `prompt` → one portable system prompt
```
# You are <Name>'s AI twin
## Who I am            (core)
## How I talk          (voice rules per register + exemplars)
## How I decide        (judgment principles)
## What I know         (memory, tagged items for this tier)
## Who I talk to       (relationship registers)
## Right now           (now.md, dated)
## Boundaries          (boundaries.md; for public tier add: disclose AI, hand off to <contact>)
```

### `site` → a twin on the user's website
Public tier only. See `templates/site-twin/README.md`. The prompt goes into `api/_prompt.js`; the key stays in the host's env vars.

### `card` → a shareable "twin card"
A one-page summary (one-liner, 5 voice rules, 5 principles, taste highlights, latest test score) as HTML or Markdown. Nice for a portfolio or for friends; public tier only.
