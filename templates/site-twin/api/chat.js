// Serverless chat endpoint for the site twin (Vercel / Netlify-style Node handler).
// The API key lives in the host's environment variables, never in browser code.
//
// Env:
//   LLM_PROVIDER = anthropic | openai   (openai = any OpenAI-compatible API: DeepSeek, Moonshot, 豆包, Groq, Ollama…)
//   LLM_API_KEY  = your key
//   LLM_MODEL    = model id (豆包: the ep-xxx endpoint id)
//   LLM_BASE_URL = optional, e.g. https://api.deepseek.com/v1 (openai provider only)
//   ALLOWED_ORIGIN = optional, e.g. https://you.github.io (cross-origin embedding)
import { TWIN_PROMPT } from "./_prompt.js";

const MAX_TURNS = 20;
const MAX_CHARS = 1000;
const hits = new Map(); // best-effort per-instance rate limit

function limited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < 60_000);
  list.push(now);
  hits.set(ip, list);
  return list.length > 12;
}

async function callAnthropic(messages) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": process.env.LLM_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: process.env.LLM_MODEL,
      max_tokens: 600,
      system: TWIN_PROMPT,
      messages,
    }),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(data?.error?.message || `HTTP ${r.status}`);
  return (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("");
}

async function callOpenAI(messages) {
  const base = (process.env.LLM_BASE_URL || "https://api.openai.com/v1").replace(/\/$/, "");
  const r = await fetch(`${base}/chat/completions`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${process.env.LLM_API_KEY}`,
    },
    body: JSON.stringify({
      model: process.env.LLM_MODEL,
      max_tokens: 600,
      messages: [{ role: "system", content: TWIN_PROMPT }, ...messages],
    }),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(data?.error?.message || `HTTP ${r.status}`);
  return data.choices?.[0]?.message?.content || "";
}

export default async function handler(req, res) {
  const origin = process.env.ALLOWED_ORIGIN;
  if (origin) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Access-Control-Allow-Headers", "content-type");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  }
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0] || "local";
  if (limited(ip)) return res.status(429).json({ error: "slow down" });

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { body = null; }
  }
  const raw = Array.isArray(body?.messages) ? body.messages : null;
  if (!raw || raw.length === 0) return res.status(400).json({ error: "messages required" });

  const messages = raw
    .slice(-MAX_TURNS)
    .filter((m) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_CHARS) }));
  while (messages.length && messages[0].role !== "user") messages.shift();
  if (!messages.length) return res.status(400).json({ error: "no user message" });

  try {
    const reply = process.env.LLM_PROVIDER === "anthropic"
      ? await callAnthropic(messages)
      : await callOpenAI(messages);
    return res.status(200).json({ reply });
  } catch (e) {
    console.error("twin chat error:", e.message);
    return res.status(502).json({ error: "the twin is unavailable right now" });
  }
}
