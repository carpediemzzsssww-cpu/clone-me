# Extraction: from materials to twin files

Goal: rules a model can follow, each backed by evidence. Not adjectives.

Bad: "Warm and humorous."
Good: "Opens replies to friends with a reaction word before content (「哈哈哈好」「啊这」), never with a greeting. — `_normalized/wechat-me.md` L33, L210, L402"

## Order and budget

1. Voice → 2. Judgment → 3. Memory → 4. Relationships → 5. Taste → 6. Now → 7. Core (write last, it's a summary) → 8. Boundaries (with the user).

Read in chunks. For large corpora, sample: the most recent 40%, the longest 20% (substance), and a random 40% (range). Note the sample in `sources.md`.

## Voice (`voice.md`)

Extract per **register** — the same person writes differently in each:
- casual chat · public posts · formal email · long-form writing · spoken (transcripts)

For each register, find:
- **Openings and closings**: how messages start and end; sign-offs.
- **Length and rhythm**: typical length; sentence length; line breaks; one thought per message or bursts.
- **Punctuation & typography**: emoji (which, how often), 「」 vs "", ellipses, exclamation marks, spaces between Chinese and English, lowercase English.
- **Word habits**: recurring words and phrases (count them; 3+ occurrences = a habit), fillers, words they never use.
- **Code-switching**: when they switch languages, which words stay in English.
- **Moves**: how they disagree, apologize, decline, ask for help, praise, joke.
- **Anti-patterns**: things that would be instantly "not me" (often clearer to the user than positive rules: ask "AI 写你的时候最让你出戏的是什么？").

Then pick **6–10 exemplar passages** (short, varied, the user's own words only) for few-shot use. Exemplars are `[private]` unless the user published them.

## Judgment (`judgment.md`)

Find decisions, preferences and arguments. For each:
- **Principle**: the rule they seem to follow ("先上线再迭代，不在没有用户的东西上打磨").
- **Evidence**: 1–2 cases with the reasoning they gave.
- **Trade-off**: what they give up for it.
- **Exceptions** they've shown.

Also extract:
- **Recurring questions** they ask (from AI chat history): what they keep trying to figure out.
- **Pushback patterns**: what makes them disagree with an AI or a person.
- **Strong opinions**: things they'd defend; things they've changed their mind on (with date — people change).

## Memory (`memory.md`)

Facts as dated, tagged lines:
```
- [public] 2026-10 · Launched Tidepool, an open-source journaling app (tidepool.example.com) · 1,200 users as of 2026-11
- [friends] 2026-09 · Moved to Lisbon for a semester
- [private] …
```
Sections: timeline · projects/works (what, role, result, link) · skills · places · beliefs that matter. Keep numbers only if a source states them; mark them with the date they were true.

## Relationships (`relationships.md`)

**Audience types, not people.** E.g. 导师/老师 · 招聘方/HR · 同事 · 好友 · 家人 · 陌生人/网友 · 客户. For each type: tone, formality, length, typical openings and closings, what they share and don't. If the user wants named people (for drafting to them), store only: name, how they know them, how they address each other, topics. No quotes from the other person.

## Taste (`taste.md`)

Loves, dislikes, and *why* when known: music, books, films, visual style, places, food, people they admire. Aggregate (top artists by year, genres) rather than full logs.

## Now (`now.md`)

This month: projects in progress, what they're learning, upcoming events (no private details of others), mood/energy if they share it, questions on their mind. Date it at the top; it goes stale fastest.

## Core (`core.md`)

- one-liner (in their voice)
- 3 versions of self-intro: 10 seconds / 30 seconds / 2 minutes
- role, current focus, what they're known for
- how the twin refers to itself

## Boundaries (`boundaries.md`)

Start from defaults in `safety.md`, then ask the user: topics to avoid, things never to reveal, what the twin may promise (usually: nothing), when to hand off, contact for handoff.

## Checks before showing each layer

- Each rule has evidence or is marked `(guess)`.
- No third-party quotes, no phone numbers / emails / addresses / IDs.
- Visibility tag on every memory / relationships / taste / now item.
- Contradictions kept, not smoothed out: "在朋友面前很碎嘴，工作邮件极短" is useful.
