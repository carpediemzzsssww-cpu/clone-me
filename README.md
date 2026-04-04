# Clone Me — AI Digital Twin Builder for Claude Code

**[中文](#中文说明) | [English](#english)**

---

## English

### What is this?

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that turns you into a chatbot. Through a guided conversation, it collects your "soul materials" — identity, personality, knowledge, writing samples — and generates:

1. **A System Prompt** — drop it into any LLM (ChatGPT, Claude, Gemini, etc.)
2. **A Chat Widget** — a self-contained HTML file you can embed on any website
3. **A Completeness Checklist** — shows what you provided and what could improve the clone

### Supported API Providers

The generated chat widget supports switching between providers at runtime:

| Provider | Endpoint |
|----------|----------|
| OpenAI | `api.openai.com/v1/chat/completions` |
| Anthropic Claude | `api.anthropic.com/v1/messages` |
| Google Gemini | `generativelanguage.googleapis.com` |
| DeepSeek | `api.deepseek.com/v1/chat/completions` |
| Groq | `api.groq.com/openai/v1/chat/completions` |
| Grok (xAI) | `api.x.ai/v1/chat/completions` |
| Together AI | `api.together.xyz/v1/chat/completions` |
| Moonshot (Kimi) | `api.moonshot.cn/v1/chat/completions` |
| Ollama (local) | `localhost:11434/v1/chat/completions` |
| Azure OpenAI | Your Azure endpoint |
| Custom / Self-hosted | Any OpenAI-compatible endpoint |

### Installation

#### Option 1: Clone the repo

```bash
git clone https://github.com/carpediemzzsssww-cpu/clone-me.git ~/.claude/skills/clone-me
```

#### Option 2: Manual copy

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/clone-me
   ```
2. Copy `SKILL.md` into that directory.

That's it. No dependencies, no config files.

### Usage

In Claude Code, type:

```
/clone-me
```

Or with a name argument:

```
/clone-me Alice
```

The skill will guide you through 6 phases:

1. **Use Case** — What's the clone for? (personal site, work delegate, knowledge clone, social persona)
2. **Identity** — Name, one-liner, role, current focus
3. **Personality & Voice** — Traits, speaking style, catchphrases
4. **Knowledge & Opinions** — Expertise, core beliefs, boundaries
5. **Writing Samples** — The most important part! Paste real things you've written
6. **Final Tuning** — Response length, language, uncertainty behavior, contact info

### Output

After the conversation, you'll get:

- **System Prompt** — copy-paste into any LLM's system prompt field
- **HTML Chat Widget** (`clone-me-[name].html`) — open in browser or embed on your site. Includes a settings panel to configure API provider and key at runtime.
- **Completeness Checklist** — see what's missing and how to improve

### Tips for Better Clones

- Provide **diverse writing samples** — casual texts, formal emails, social posts, long-form writing
- The more you give, the better the voice matching
- Include **opinions and hot takes** — they make the clone feel real
- Update your clone periodically as your focus and thinking evolve

---

## 中文说明

### 这是什么？

一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 技能，通过对话采集你的"灵魂素材"——身份、性格、知识、写作样本——然后生成：

1. **System Prompt** — 直接粘贴到任何 LLM（ChatGPT、Claude、Gemini 等）
2. **聊天组件** — 一个独立 HTML 文件，可嵌入任何网站
3. **素材完整度清单** — 展示已采集和待补充的内容

### 支持的 API 服务商

生成的聊天组件支持运行时切换服务商：

| 服务商 | 接口地址 |
|--------|----------|
| OpenAI | `api.openai.com/v1/chat/completions` |
| Anthropic Claude | `api.anthropic.com/v1/messages` |
| Google Gemini | `generativelanguage.googleapis.com` |
| DeepSeek（深度求索） | `api.deepseek.com/v1/chat/completions` |
| Groq | `api.groq.com/openai/v1/chat/completions` |
| Grok (xAI) | `api.x.ai/v1/chat/completions` |
| Together AI | `api.together.xyz/v1/chat/completions` |
| Moonshot（Kimi） | `api.moonshot.cn/v1/chat/completions` |
| Ollama（本地） | `localhost:11434/v1/chat/completions` |
| Azure OpenAI | 你的 Azure 端点 |
| 自定义 / 自部署 | 任何 OpenAI 兼容接口 |

### 安装

#### 方式一：克隆仓库

```bash
git clone https://github.com/carpediemzzsssww-cpu/clone-me.git ~/.claude/skills/clone-me
```

#### 方式二：手动复制

1. 创建技能目录：
   ```bash
   mkdir -p ~/.claude/skills/clone-me
   ```
2. 将 `SKILL.md` 复制到该目录下。

搞定。无依赖，无需额外配置。

### 使用方法

在 Claude Code 中输入：

```
/clone-me
```

也可以带名字参数：

```
/clone-me 小明
```

技能会引导你完成 6 个阶段：

1. **用途** — 克隆用来做什么？（个人网站、工作代理、知识分身、社交人设）
2. **身份** — 名字、一句话介绍、角色、当前关注点
3. **性格与语气** — 性格特质、说话风格、口头禅
4. **知识与观点** — 专业领域、核心信念、边界话题
5. **写作样本** — 最重要的一步！粘贴你真实写过的文字
6. **最终调校** — 回复长度、语言、不确定时的表现、联系方式

### 输出

对话结束后，你会得到：

- **System Prompt** — 复制粘贴到任何 LLM 的系统提示词字段
- **HTML 聊天组件**（`clone-me-[名字].html`）— 浏览器打开或嵌入网站，内置设置面板可配置 API 服务商和密钥
- **素材完整度清单** — 查看缺失项和改进建议

### 让克隆更像你的技巧

- 提供**多样的写作样本** — 随意的聊天、正式的邮件、社交帖子、长文
- 给的越多，语气匹配越准
- 加入**观点和态度** — 这是让克隆有"人味"的关键
- 定期更新你的克隆，因为你的关注点和想法在变化

---

## License

MIT
