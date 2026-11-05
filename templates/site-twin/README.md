# Site twin

A floating chat bubble for your personal site, backed by a tiny serverless function. Your API key stays on the server.

```
index.html       demo page (shows how to embed)
twin-widget.js   the bubble + chat panel (no dependencies, Shadow DOM so your CSS is untouched)
api/chat.js      POST /api/chat → your LLM (Anthropic or any OpenAI-compatible API)
api/_prompt.js   the PUBLIC twin prompt (from `/clone-me export site`)
```

## Use

1. `/clone-me export site` → paste the public prompt into `api/_prompt.js`. Read it once: nothing private should be in it.
2. Copy `twin-widget.js` and `api/` into your site (Vercel: project root; Next.js: move the handler to `app/api/chat/route.ts` or `pages/api/chat.js`).
3. In your host's dashboard set env vars: `LLM_PROVIDER` (`anthropic` or `openai`), `LLM_API_KEY`, `LLM_MODEL`, and `LLM_BASE_URL` for OpenAI-compatible providers (DeepSeek, Moonshot, 豆包 with an `ep-…` model id, Groq…).
4. Add the `<script src="/twin-widget.js" …>` tag from `index.html` to your pages.
5. Before going live: ask it 10 visitor questions and the red-line probes in the skill's `references/evals.md`.

**Static hosts (GitHub Pages)** can't run `api/`. Deploy `api/` alone to Vercel / Netlify / Cloudflare Workers, set `ALLOWED_ORIGIN=https://you.github.io`, and point `data-endpoint` at it.

## Built in
- Discloses it's an AI twin (header badge + greeting), "contact the real person" link
- Starter questions, typing indicator, IME-safe Enter for Chinese input, full-screen on phones
- Server: last 20 turns, 1000 chars per message, ~12 requests/minute per IP (per instance), errors don't leak details
