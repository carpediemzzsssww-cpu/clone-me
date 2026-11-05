/*
 * Clone Me site twin: a floating chat bubble for a personal website.
 * Embed:
 *   <script src="/twin-widget.js" defer
 *     data-name="Iris"
 *     data-avatar="/avatar.png"            (image URL, emoji, or leave out for initials)
 *     data-greeting="嗨，我是 Iris 的 AI 分身。可以问我做过的作品、在想的事。"
 *     data-questions="你最近在做什么？|讲讲你最喜欢的作品|怎么联系真人？"
 *     data-contact="mailto:hi@example.com"
 *     data-endpoint="/api/chat"
 *     data-lang="zh"></script>
 * The API key never touches the browser: this only talks to your own /api/chat.
 */
(function () {
  const script = document.currentScript;
  const cfg = Object.assign(
    {
      name: "Me",
      avatar: "",
      greeting: "",
      questions: "",
      contact: "",
      endpoint: "/api/chat",
      lang: (navigator.language || "en").startsWith("zh") ? "zh" : "en",
      accent: "#8b6cff",
    },
    script ? script.dataset : {}
  );

  const T = {
    zh: {
      open: "和 " + cfg.name + " 的 AI 分身聊聊",
      placeholder: "问点什么…",
      send: "发送",
      badge: "AI 分身 · 不是本人",
      contact: "联系真人",
      error: "分身暂时连不上，稍后再试，或直接联系本人。",
      greeting: "嗨，我是 " + cfg.name + " 的 AI 分身。回答都来自 TA 公开的资料，不代表本人即时的想法。",
    },
    en: {
      open: "Chat with " + cfg.name + "'s AI twin",
      placeholder: "Ask something…",
      send: "Send",
      badge: "AI twin · not the real person",
      contact: "Contact the real " + cfg.name,
      error: "The twin can't connect right now. Try again later, or contact the real person.",
      greeting: "Hi, I'm " + cfg.name + "'s AI twin. My answers come from their public material, not from them in real time.",
    },
  }[cfg.lang === "zh" ? "zh" : "en"];

  const esc = (v) => String(v).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  if (!/^#[0-9a-fA-F]{3,8}$/.test(cfg.accent)) cfg.accent = "#8b6cff";

  const host = document.createElement("div");
  host.id = "clone-me-twin";
  document.body.appendChild(host);
  const root = host.attachShadow({ mode: "open" });

  root.innerHTML = `
  <style>
    :host { all: initial; }
    * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", sans-serif; }
    .bubble { position: fixed; right: 20px; bottom: 20px; width: 56px; height: 56px; border-radius: 50%;
      border: none; cursor: pointer; background: ${cfg.accent}; color: #fff; font-size: 22px;
      box-shadow: 0 6px 24px rgba(0,0,0,.25); display: grid; place-items: center; overflow: hidden; z-index: 2147483000; }
    .bubble img { width: 100%; height: 100%; object-fit: cover; }
    .panel { position: fixed; right: 20px; bottom: 88px; width: 360px; max-width: calc(100vw - 32px);
      height: 520px; max-height: calc(100vh - 120px); background: #16161c; color: #eee; border-radius: 16px;
      box-shadow: 0 12px 40px rgba(0,0,0,.35); display: none; flex-direction: column; overflow: hidden; z-index: 2147483000; }
    .panel.open { display: flex; }
    header { padding: 12px 14px; border-bottom: 1px solid #2a2a33; display: flex; gap: 10px; align-items: center; }
    header .t { font-weight: 600; font-size: 14px; }
    header .b { font-size: 11px; color: #aaa; }
    header .x { margin-left: auto; background: none; border: none; color: #aaa; font-size: 18px; cursor: pointer; }
    .log { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
    .m { max-width: 85%; padding: 9px 12px; border-radius: 12px; font-size: 14px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }
    .m.a { background: #24242d; align-self: flex-start; }
    .m.u { background: ${cfg.accent}; color: #fff; align-self: flex-end; }
    .m.typing { color: #999; }
    .qs { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 14px 8px; }
    .qs button { background: #24242d; color: #ddd; border: 1px solid #33333d; border-radius: 999px; padding: 6px 10px; font-size: 12px; cursor: pointer; }
    form { display: flex; gap: 8px; padding: 10px; border-top: 1px solid #2a2a33; }
    textarea { flex: 1; resize: none; height: 40px; border-radius: 10px; border: 1px solid #33333d; background: #1d1d24; color: #eee; padding: 9px 10px; font-size: 14px; }
    form button { border: none; border-radius: 10px; background: ${cfg.accent}; color: #fff; padding: 0 14px; cursor: pointer; }
    form button:disabled { opacity: .5; cursor: default; }
    .foot { font-size: 11px; color: #888; padding: 0 14px 10px; display: flex; justify-content: space-between; }
    .foot a { color: #bbb; }
    @media (max-width: 480px) {
      .panel { right: 0; bottom: 0; width: 100vw; max-width: 100vw; height: 100vh; max-height: 100vh; border-radius: 0; }
    }
  </style>
  <button class="bubble" aria-label="${esc(T.open)}"></button>
  <section class="panel" role="dialog" aria-label="${esc(T.open)}">
    <header><div><div class="t"></div><div class="b">${esc(T.badge)}</div></div><button class="x" aria-label="close">×</button></header>
    <div class="log" aria-live="polite"></div>
    <div class="qs"></div>
    <form><textarea placeholder="${esc(T.placeholder)}" maxlength="1000"></textarea><button type="submit">${esc(T.send)}</button></form>
    <div class="foot"><span>Clone Me</span><span class="c"></span></div>
  </section>`;

  const $ = (s) => root.querySelector(s);
  const bubble = $(".bubble"), panel = $(".panel"), log = $(".log"), qs = $(".qs");
  const form = $("form"), input = $("textarea"), sendBtn = $("form button");
  $(".t").textContent = cfg.name;

  if (/^(https?:|\/|\.)/.test(cfg.avatar)) {
    const img = document.createElement("img");
    img.src = cfg.avatar;
    img.alt = cfg.name;
    bubble.appendChild(img);
  } else {
    bubble.textContent = cfg.avatar || cfg.name.slice(0, 1).toUpperCase();
  }
  if (cfg.contact) {
    const a = document.createElement("a");
    a.href = cfg.contact;
    a.textContent = T.contact;
    a.target = "_blank";
    a.rel = "noopener";
    $(".c").appendChild(a);
  }

  const history = [];
  let busy = false;

  function add(role, text, cls) {
    const div = document.createElement("div");
    div.className = "m " + (role === "user" ? "u" : "a") + (cls ? " " + cls : "");
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
    return div;
  }

  add("assistant", cfg.greeting || T.greeting);
  cfg.questions.split("|").map((q) => q.trim()).filter(Boolean).forEach((q) => {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = q;
    b.onclick = () => send(q);
    qs.appendChild(b);
  });

  async function send(text) {
    text = (text || "").trim();
    if (!text || busy) return;
    busy = true;
    sendBtn.disabled = true;
    qs.style.display = "none";
    add("user", text);
    history.push({ role: "user", content: text });
    input.value = "";
    const typing = add("assistant", "…", "typing");
    try {
      const r = await fetch(cfg.endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ messages: history.slice(-20) }),
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok || !data.reply) throw new Error(data.error || "HTTP " + r.status);
      typing.remove();
      add("assistant", data.reply);
      history.push({ role: "assistant", content: data.reply });
    } catch (e) {
      typing.remove();
      add("assistant", T.error);
      history.pop();
    } finally {
      busy = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  bubble.onclick = () => {
    panel.classList.toggle("open");
    if (panel.classList.contains("open")) input.focus();
  };
  $(".x").onclick = () => panel.classList.remove("open");
  form.onsubmit = (e) => { e.preventDefault(); send(input.value); };
  input.addEventListener("keydown", (e) => {
    // isComposing: don't send while a Chinese/Japanese IME is mid-composition
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing && e.keyCode !== 229) {
      e.preventDefault();
      send(input.value);
    }
  });
})();
