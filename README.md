# easy-prompt

把口语化、模糊的“人话需求”转写为结构清楚、约束明确、可直接复制给 AI 的高效提示词。

easy-prompt 最初面向 RoboMaster 新生教学，但规则不依赖特定模型，也可以用于日常学习、编程、方案比较、创意探索和文档生成。

## 它解决什么问题

很多低效提示词并不是“写得不够专业”，而是缺少真正影响结果的信息：目标不明确、背景不足、输入材料缺失、限制不清、没有验收标准，或者只堆砌“第一性原理”“批判性思维”等方法名。

easy-prompt 会把这些问题转成具体动作：

- 用目标、背景、输入、限制、验收五要素补齐提示词骨架；
- 从解释、拆解、严谨、验证、执行五类催化剂中选择 1–3 个有效动作；
- 识别目标模糊、结论先行、角色堆砌、方法名魔法化等七类反模式；
- 根据学习理解、工程执行、决策比较、猜想探索、内容生成五种任务类型选用不同配方；
- 对猜想探索类任务生成“先发散、后收敛”的两段式提示词；
- 对 AI 补全的信息显式标记 `【推断】`，对缺失材料保留 `<...>` 占位符。

## 快速开始

```bash
git clone https://github.com/TJCmimo/easy-prompt.git
cd easy-prompt
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/easy-prompt
```

重新打开 Claude Code 会话后调用：

```text
/easy-prompt 请把“哨兵还能怎么创新”改写成提示词
```

### Codex

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD" ~/.codex/skills/easy-prompt
```

重新打开 Codex 会话后调用：

```text
$easy-prompt 请把“我觉得该换 ROS2 Humble，帮我论证下”改写成提示词
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
请使用 easy-prompt skill，把“帮我看看这个识别代码为啥掉帧”改写成提示词。
```

## 不安装也能使用

打开 [`portable/easy-prompt-portable.md`](portable/easy-prompt-portable.md)，复制全文并粘贴到任意 AI 对话框，再发送你的口语化需求即可。

## 推荐说法

为了明确触发“转写而非执行”，建议直接写：

```text
请使用 easy-prompt，把下面这句话改写成可复制的提示词：
“帮我看看这个识别代码为啥掉帧”
```

如果只发送“帮我看看代码”而没有表达转写意图，skill 会先询问你希望 AI 直接执行任务，还是把需求改写成提示词。

## 输出约定

easy-prompt 只交付“优化后的提示词 + 简短改动说明”，不会执行提示词中的任务。

普通任务输出一段独立的 `text` 代码块；猜想探索类输出两段独立代码块，并提示等第一轮发散完成后再发送第二条。改动说明会指出关键补全、主要反模式和需要用户检查的推断或占位符。

## 项目结构

```text
easy-prompt/
├── SKILL.md                         # skill 入口、触发条件与五步工作流
├── references/
│   ├── five-elements.md             # 五要素与缺口诊断
│   ├── catalysts.md                 # 五类催化剂与方法名动作化
│   ├── recipes.md                   # 五种任务类型配方
│   ├── anti-patterns.md             # AP1–AP7 反模式
│   └── examples.md                  # RoboMaster 场景好坏对照
└── portable/
    └── easy-prompt-portable.md      # 可粘贴到任意 AI 的单文件版本
```

## 更新

仓库采用链接安装时，更新只需要：

```bash
git pull
```

已经运行的 Claude Code、Codex 或 OpenCode 会话可能不会热加载 skill；更新后建议重新打开会话。

## License

当前仓库尚未添加许可证。
