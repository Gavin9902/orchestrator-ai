[English](README_EN.md) | **中文**

# Orchestrator v2.0 · Worker-Checker Couple

> AI 质量保障系统 2.0。把 v1 的「一个 Worker 做全部」升级为「多个 Worker-Checker Couple 并行协作」。
> Worker 间文件交接，loop.py 纯代码调度，三层防作弊。

> "They just don't work. It's slop." — **Andrej Karpathy**，OpenAI 联合创始人。
>
> "AI 能搞定 70%，剩下 30% 一样难。" — **Addy Osmani**，Google Chrome 工程总监。

**问题不在模型不够强。在没人帮模型检查。**

![Orchestrator Pitch](pitch.gif)

## v2.0 vs v1.0

| 维度 | v1.0 | v2.0 |
|------|------|------|
| Worker 粒度 | 一个 Worker 做全部 | 拆成多个最小 Couple |
| 调度层 | Orch 直接调度 | loop.py 生成指令 → Orch 机械执行 |
| 任务拆解 | Orch 拆 | PM Couple 拆 |
| 并行 | 不支持 | 同层 Couple 并行 |
| 文件交接 | 无要求 | 强制文件路径传递 |
| Orch 权限 | 全权 | 只做翻译 + 机械传递 + 展示 |
| 防作弊 | 基础 | 三层防御（魔法叙事 + 结构隔离 + 代码校验） |
| 多平台 | Claude Code | CodeBuddy / Claude Code / Codex CLI / 通用 |

## 核心理念

> 一个 Worker 只做一类事、只用一个能力、只通过文件交接。

```
用户 → Orch（信使）→ loop.py（建筑师）→ 并行 Couple 群
                                          ├── Couple A: 生产 Worker → 检查 Worker → judge.py
                                          ├── Couple B: 生产 Worker → 检查 Worker → judge.py
                                          └── Couple C: 生产 Worker → 检查 Worker → judge.py
```

**信使契约**：Orch 不是被"限制"——是自愿履行契约。不能创造、不能评判、不能规划。只能传递。

## 多平台支持

加载 skill 时自动询问你所在的平台：

| 平台 | 状态 |
|------|------|
| CodeBuddy | ✅ 开箱即用 |
| Claude Code | ✅ 开箱即用 |
| OpenAI Codex CLI | ✅ 开箱即用 |
| 其他 / 不确定 | 🌱 自生生长（Orch 自行探测工具后映射） |

## 快速开始

**1. 安装**

把 GitHub 链接丢给你的 AI 编程助手：

```
安装这个 skill：https://github.com/Gavin9902/orchestrator-ai
```

**2. 召唤**

```
/orch-worker-couple
```

或触发词：`couple`、`worker-couple`、`拆任务`、`并行Worker`、`文件交接`

**3. 聊需求**

Orch 引导你梳理清楚要做什么。PM Couple 自动拆解任务图。

**4. 等结果**

loop.py 调度并行 Couple 执行。你随时问进度。

**5. 确认交付**

所有 Couple 通过 judge.py 判官审核后，Orch 展示结果。你点头才算交付。

## 架构文档

| 文档 | 内容 |
|------|------|
| `core/ARCHITECTURE.md` | 角色模型、防作弊体系、Worker 拆分原则 |
| `core/PROTOCOLS.md` | 数据格式、Action 类型、状态机、loop.py 接口 |
| `codebuddy/SKILL.md` | CodeBuddy 平台专用版 |
| `claude-code/SKILL.md` | Claude Code 平台专用版 |
| `codex/SKILL.md` | Codex CLI 平台专用版 |
| `generic/SKILL.md` | 通用版（自生生长） |

## 防作弊三层防御

```
🪄 第一层 · 魔法叙事 — 信使契约 + 五步呼吸 + 冲动协议
🔒 第二层 · 结构隔离 — 文件交接 + 上下文隔离 + 互不知晓
🔐 第三层 · 代码校验 — action_hash + orch_receipt + checksum + .lock
```

覆盖 20 条作弊路径，详见 `core/ARCHITECTURE.md`。

## v1.0 存档

v1.0 版本（orchestrator 原版）保留在 `v1/` 目录中，仍可使用。

## License

MIT
