# Ian XHS Carousel

**中文** | [English](README.en.md)

> 把文章、案例或笔记，排成一组 3:4 的小红书图文。
>
> 1080×1440 竖版 | 20 个母版 | 浅色 / 深色 | Claude Code Skill

---

## 这是什么

Ian XHS Carousel 是一个 AI Skill，把你的内容做成一组小红书轮播图，风格是简洁的产品界面风。

你把内容交给它，它先出一张分镜表给你确认，确认后再排版、出图。

**最好用 Claude 跑。**

---

## 适合谁用

- 写文章、做案例拆解，想顺手发一份小红书图文的人
- 做 AI、产品、设计、效率工具内容，图里常有截图、步骤、对比、数据、代码的人
- 想让每期图文风格统一、看着干净的人

想要手绘、插画、大色块海报这类风格的话，这个不太合适。

---

## 它会产出什么

- **分镜表**：每页讲什么、用哪个母版、标题怎么写，先给你确认
- **每页一张 PNG**：1080×1440，可以直接发
- **总览图**：所有页排在一起，一眼看整组节奏
- **HTML 源文件**：想自己改字、换图，改完重新渲染就行

浅色、深色两版都能出，版式一样。

小红书帖子的标题、正文和话题标签需要你另外写。

---

## 20 个母版

![20 个母版 · 浅色](examples/images/templates-light.png)

<details>
<summary>深色版</summary>

![20 个母版 · 深色](examples/images/templates-dark.png)

</details>

| 分组 | 母版 |
|---|---|
| 封面 | T01 对话框、T02 窗口、T03 通知 |
| 讲做法 | T04 步骤、T05 清单、T06 时间线 |
| 对比 | T07 对错、T08 前后双栏 |
| 展示 | T09 宫格、T10 截图标注、T11 手机截图、T12 应用列表 |
| 数字 | T13 数据指标、T14 参数设置 |
| 文字 | T15 观点大字、T16 聊天、T17 提示词、T18 代码 |
| 结尾 | T19 对照、T20 完成 |

20 个都不合适的时候，AI 会用同一套样式拼一个新排法。

---

## 安装

**1. 下载并复制到 Claude Code**

```bash
git clone https://github.com/helloianneo/ian-xhs-carousel.git
mkdir -p ~/.claude/skills
cp -R ./ian-xhs-carousel/ian-xhs-carousel ~/.claude/skills/
```

**2. 装渲染要用的工具**（第一次用时装一次）

```bash
pip install playwright pillow
playwright install chromium
```

渲染时会联网加载英文和代码字体，记得保持网络畅通。

---

## 素材要好看

一组图好不好看，很大程度看你给的素材。上传前花几分钟挑一挑：

- **截图**：用高清的，裁掉浏览器工具栏、桌面和别的窗口；做深色版就截深色模式的
- **Logo 和图标**：用官方的 SVG，别截一个小图再放大
- **照片和效果图**：一堆里挑最好看的那张
- **没有好图**：先空着，它会在分镜表里列出来问你要，别拿糊的凑

---

## 怎么用

在 Claude Code 里输入：

```text
/ian-xhs-carousel 把下面这篇文章做成一组小红书图文。

<粘贴文章>
```

不输命令也行，直接说"把这篇做成小红书"，它一般会自己用上。

**只要分镜表**

```text
/ian-xhs-carousel 先别排版，帮我看看下面这篇能做成几页，出分镜表就行。

<粘贴文章>
```

**出深色版**

```text
/ian-xhs-carousel 把这篇做成小红书图文，用深色主题。截图在 ./shots 里。

<粘贴文章>
```

**改某一页**

```text
第 3 页换成 T08 前后双栏，左边放旧版截图，右边放新版。
```

更多示例见 [examples/prompts.md](examples/prompts.md)。

---

## 工作流程

1. **读内容**：想清楚这组图要让人带走什么
2. **出分镜表**：一页讲一件事，一般 5 页左右，**停下来等你确认**
3. **准备配图**：用你给的素材，缺的会列出来问你
4. **排版**：从 20 个母版里挑合适的
5. **渲染和自查**：检查文字溢出、字号、配色，有问题自己改掉
6. **交付**：给你每页图和总览图

---

## 小贴士

- 分镜表那一步多花点时间，页数和每页讲什么定下来，后面基本不用返工
- 图上的字越少越好，说不完的留给正文
- 页数宁少勿多，5 页左右刚好

---

## 目录结构

```text
.
├── README.md
├── README.en.md
├── examples/              母版总览图、更多提示词
└── ian-xhs-carousel/      ← 安装的是这个文件夹
    ├── SKILL.md
    ├── assets/            样式、母版、图标
    ├── references/        设计规则、母版说明、自查清单
    └── scripts/           渲染脚本
```

---

## 相关项目

- [Ian Xiaohei Illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations) — 中文小黑怪诞正文配图生成 Skill
- [Ian Handdrawn PPT](https://github.com/helloianneo/ian-handdrawn-ppt) — 中文手绘技术 PPT-style 页面图生成 Skill
- [Awesome Claude Code Skills](https://github.com/helloianneo/awesome-claude-code-skills) — Claude Code Skills / Agents / Plugins 精选合集
- [Obsidian + Claude AI Second Brain](https://github.com/helloianneo/obsidian-ai-second-brain) — Obsidian + Claude AI 个人知识库搭建指南

---

## 关于作者

**Ian (伊恩)** — 产品设计师 / AI Builder

GitHub 万星、Dribbble 万粉，用 AI 做好玩的东西，探索 AI + 自由。

- 网站：[ianneo.xyz](https://www.ianneo.xyz)
- X/Twitter：[@ianneo_ai](https://x.com/ianneo_ai)
- GitHub：[helloianneo](https://github.com/helloianneo)
- Indie Builders 社群：[ianneo.xyz/ib](https://ianneo.xyz/ib)

交流合作加我微信，备注来意：

<p>
  <img src="assets/ian-wechat-qr.jpg" alt="Ian 微信二维码" width="120">
</p>

扫不了就搜微信号 `ianneoxyz`。

---

## License

MIT License. See [LICENSE](LICENSE).
