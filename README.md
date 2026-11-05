# Clone Me

**[中文](#中文) | [English](#english)**

---

## 中文

**数字分身不是一张人设卡，是一个你朋友都猜不出来的你。**

人设卡写着「我很幽默」。分身能替你写出那封你会写的邮件：给这个人，聊这件事，用你的语气。Clone Me 用你自己的数据做分身，不靠问卷：发出去的邮件、自己说过的话、发过的帖子、和 AI 的对话、笔记、日历。然后用盲测证明它像你，再让它去干活。

### 三个入口

| 你是 | 用法 |
|---|---|
| Claude Code / Codex 用户 | 装成 skill，输入 `/clone-me`。能读本机文件、接 Gmail / 日历 / Notion / GitHub 等连接器，能直接部署网站分身 |
| Claude.ai 用户 | 把这个文件夹打包上传成 skill |
| 任何 AI 聊天应用（ChatGPT、豆包、Kimi、DeepSeek…） | 打开 [PROMPT.md](PROMPT.md)，复制粘贴，跟着走。不用装任何东西 |

### 分身由 8 层组成

核心 · **语气** · **判断** · 记忆 · 关系 · 品味 · 最近 · 边界

每条语气和判断规则都附上你的原话当依据；每条记忆都标 `[公开]` `[朋友]` `[私密]`，放到网站上的只会是公开那部分。

### 数据从哪来

[数据接入地图](references/data-sources.md) 列了 40 多个来源，每个都写清楚：怎么拿到（导出文件 / 本机读取 / 连接器 / 浏览器读自己的主页 / 自己的 API token）、要给什么权限、敏感程度（🟢🟡🔴）、能喂哪一层。几个容易被忽略的好来源：

- **发件箱**：带着收件人类型的正式语气（给导师、给 HR、给朋友，写法完全不同）
- **你和 ChatGPT / Claude 的对话导出**：你反复在问什么、怎么反驳，是「判断」层最好的镜子
- **Claude Code 的 `CLAUDE.md` 和记忆**：如果你写过，那其实已经是一个手工做的分身
- **朋友的三句话**：「用三个词形容我 / 我最常说什么 / 我什么时候最像我」

[scripts/materials.py](scripts/materials.py) 会把 ChatGPT、Claude.ai、Telegram、WhatsApp、邮箱 mbox、X 存档、普通聊天 txt 转成**只保留你自己说的话**的文本，并且默认抹掉手机号、邮箱、证件号。

### 分身能做什么

| 替我（对外） | 懂我（对内） | 超出我 |
|---|---|---|
| 介绍我：任何对象、任何长度 | 第二大脑：「我去年怎么看 X？」带出处 | 时间胶囊：每年存一份，和去年的自己聊 |
| 替我联络：给想认识的人写第一封邮件 / 私信 | 决策镜子：换我会怎么选，以及我在哪里自相矛盾 | 分身对谈：两个人的分身先聊一轮，找合作点 |
| 收件箱分身：分拣邮件，按关系起草回复 | 周回顾：用我的语气写本周小结 | 产品客服：给你的产品也做一个分身 |
| 社媒分身：把碎碎念变成帖子，起草评论回复 | AI 底座：让 Claude、ChatGPT、豆包都认识我 | |
| 网站分身：个人网站右下角的「我」 | 求职：按 JD 改简历、模拟面试 | |

素材不够时，会用**解锁表**告诉你「再给最近 50 封发出去的邮件，就能解锁替我联络」，而不是让你填完一张表。

### 命令

```
/clone-me                 新建，或继续已有的分身
/clone-me feed            加素材，看新解锁了什么
/clone-me test            盲测 + 红线测试，被认出来的地方变成新规则
/clone-me use outreach    让分身干活（intro / outreach / inbox / social / site / career / brain / decide / weekly …）
/clone-me export skill    导出成 skill / CLAUDE.md / AGENTS.md / ChatGPT / Claude Project / 豆包智能体 / 网站
/clone-me snapshot        存一份今年的分身，对比「我变了什么」
```

### 几条不会松动的规矩

- **只起草，不发送。** 邮件、私信、评论、发帖都由你点头才发；能建草稿就不直接发送。
- **原始素材只留在你的电脑上**（`materials/` 不进 git、不进任何导出）。别人说的话不会被学进分身。
- **默认只克隆你自己。** 克隆别人要对方同意。
- **对别人说话时承认自己是 AI 分身**，不替你答应任何事，不知道就说不知道。

### 安装

```bash
git clone https://github.com/carpediemzzsssww-cpu/clone-me.git ~/.claude/skills/clone-me
```

Codex：把同一个仓库克隆到 `~/.codex/skills/clone-me`。

### 目录

```
SKILL.md                    主流程
PROMPT.md                   普通人版：粘贴进任何 AI 聊天应用
references/                 数据接入地图、提炼方法、应用场景、盲测、安全、导出
templates/twin/             分身包模板（8 层 + 来源记录 + 盲测）
templates/site-twin/        网站分身：浮动聊天组件 + 服务端接口（key 不进浏览器）
scripts/materials.py        素材扫描和转换（Python 3.9+，无依赖）
```

---

## English

**A digital twin isn't a persona card. It's a version of you your friends can't tell apart.**

A persona card says "I'm witty". A twin writes the email you'd write, to this person, about this thing. Clone Me builds the twin from your own data instead of a questionnaire (sent mail, your side of chats, posts, AI chat history, notes, calendar), proves likeness with a blind test, then puts it to work.

**Three ways in.** Claude Code / Codex: install as a skill and run `/clone-me` (local files, connectors such as Gmail, Calendar, Notion and GitHub, website deploys). Claude.ai: upload the folder as a skill. Any chat AI: paste [PROMPT.md](PROMPT.md) (written in Chinese; the AI will follow your language).

**Eight layers:** core, voice, judgment, memory, relationships, taste, now, boundaries. Voice and judgment rules cite your own words as evidence; memory items are tagged public / friends / private, and only public items reach anything other people talk to.

**Data map.** [references/data-sources.md](references/data-sources.md) covers 40+ sources: how to get each one, the permission it needs, how sensitive it is, and which layer it feeds. [scripts/materials.py](scripts/materials.py) converts ChatGPT / Claude.ai / Telegram / WhatsApp / mbox / X archive / plain chat logs to your-words-only text and redacts phone numbers, emails and ID numbers.

**What it does.** Introduce you for any audience · draft outreach emails and DMs · triage your inbox · draft posts and replies · a twin on your personal site · resume and interview prep · a second brain with sources · a decision mirror · weekly reviews · make every AI tool know you · yearly time capsules · twin-to-twin conversations.

**Rules.** Draft, never send without your yes. Raw materials stay on your machine. Other people's words are never learned. Yourself by default; anyone else only with consent. When it talks to others, it says it's an AI twin.

```bash
git clone https://github.com/carpediemzzsssww-cpu/clone-me.git ~/.claude/skills/clone-me
```

## License

MIT
