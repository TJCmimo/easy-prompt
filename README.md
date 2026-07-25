# easy-prompt

> 把口语化、模糊的“人话需求”，转写成结构清楚、约束明确、可直接复制给 AI 的提示词。

`easy-prompt` 是一个不绑定特定模型或任务领域的 AI skill，适用于日常学习、编程、方案比较、创意探索和文档生成。它只交付优化后的提示词与简短改动说明，不会代替你执行提示词中的任务。

想立即开始？你可以[选择对应环境安装](#快速开始)，也可以[直接使用可移植版](#不安装也能使用)。

## 它解决什么问题

很多提示词效果不理想，并不是因为表达“不够专业”，而是缺少真正影响结果的信息：目标不明确、背景不足、任务材料缺失、限制不清、没有验收标准，或者只堆砌“第一性原理”“批判性思维”等方法名。

`easy-prompt` 会识别这些缺口，把模糊要求转成 AI 可以执行和检查的具体动作，同时尽量减少不必要的假设。

## 核心亮点

- **补齐关键信息**：逐项检查目标、背景、材料、限制、验收；背景只在会实质改变答案时保留，不默认推断用户身份或能力。
- **把方法变成动作**：按学习理解、工程执行、决策比较、猜想探索和内容生成五种任务类型选择配方，并从解释、拆解、严谨、验证和执行五类催化剂中选取 1–3 个有效动作。
- **主动发现偏差与遗漏**：识别 AP1–AP8 八类反模式，优先使用可逐项检查的正向标准；需要时借助耗时预算表、状态转移表、资源平衡表、坐标表等真实领域结构组织信息，无法确认的内容标记为“待验证”。
- **提供独立反方审查**：推荐审查说明最终推荐是否改变，筛选审查说明候选集是否改变，指定方案反驳默认说明原判断是否改变；只比较时不触发。环境支持多 agent 时派发独立批评者，否则执行隔离的红队复核。
- **处理复杂探索与长会话**：猜想探索采用“先发散、后收敛”的两段式提示词；术语不明时使用“引导采样 → 上下文回滚”；长任务通过主线锚点减少语义漂移，并可收割当前会话中已经确认的路径、报错、命令和修改。
- **保持输出可复制、少假设**：简单任务可以输出 2–3 行自然语句，复杂任务保留清晰字段；AI 补全的信息标记为 `【推断】`，缺失材料保留 `<...>` 占位符。

## 快速开始

先克隆仓库：

```bash
git clone https://github.com/TJCmimo/easy-prompt.git
cd easy-prompt
```

然后选择你的使用环境。

### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/easy-prompt
```

重新打开 Claude Code 会话后调用：

```text
/easy-prompt 请把“我们的社区读书会还能怎么创新”改写成提示词
```

### Codex

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/easy-prompt
```

重新打开 Codex 会话后调用：

```text
$easy-prompt 请把“我觉得应该选方案 A，帮我论证一下”改写成提示词
```

### OpenCode

在 `~/.config/opencode/opencode.json` 顶层合并下面的配置，并把路径替换为仓库的绝对路径：

```json
{
  "skills": {
    "paths": ["/absolute/path/to/easy-prompt"]
  }
}
```

重启 OpenCode 后，在对话中明确点名：

```text
请使用 easy-prompt skill，把“帮我把这份活动复盘写得更清楚”改写成提示词。
```

## 不安装也能使用

打开 [`portable/easy-prompt-portable.md`](portable/easy-prompt-portable.md)，复制全文并粘贴到任意 AI 对话框，再发送你的口语化需求即可。

## 使用说明

### 明确触发“转写”

为了避免 AI 直接执行原任务，建议明确说明你需要的是提示词：

```text
请使用 easy-prompt，把下面这句话改写成可复制的提示词：
“帮我比较这三种学习方案”
```

如果只发送“帮我看看这个方案”而没有表达转写意图，skill 会先询问你希望 AI 直接执行任务，还是把需求改写成提示词。

### 你会得到什么

`easy-prompt` 只交付“优化后的提示词 + 简短改动说明”：

- 普通任务输出一段独立的 `text` 代码块；
- 猜想探索类任务输出“先发散、后收敛”的两段独立代码块，并提示何时发送第二条；
- 改动说明会指出关键补全、主要反模式，以及需要检查的 `【推断】` 或 `<...>` 占位符。

## 项目文档

- [`SKILL.md`](SKILL.md)：触发边界、五步工作流与输出契约。
- [`references/five-elements.md`](references/five-elements.md)：目标、背景、材料、限制和验收的缺口诊断。
- [`references/catalysts.md`](references/catalysts.md)：五类提示词催化剂，以及方法名到具体动作的转换。
- [`references/recipes.md`](references/recipes.md)：五种任务类型配方与两段式工作流。
- [`references/domain-structures.md`](references/domain-structures.md)：用于发现遗漏维度的领域结构。
- [`references/anti-patterns.md`](references/anti-patterns.md)：AP1–AP8 反模式及纠正方式。
- [`references/examples.md`](references/examples.md)：跨领域示例与输出合同对照。
- [`tests/test_skill_contract.py`](tests/test_skill_contract.py)：通用化与核心行为契约测试。

## 更新

仓库采用链接安装时，更新只需要：

```bash
git pull
```

已经运行的 Claude Code、Codex 或 OpenCode 会话可能不会热加载 skill；更新后建议重新打开会话。

## 许可证

当前仓库尚未添加许可证。
