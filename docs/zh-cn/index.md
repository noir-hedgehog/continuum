---
layout: default
title: Continuum 中文
---

<div class="language-switch">
  <a class="language-pill" href="/continuum/">English</a>
  <a class="language-pill active" href="/continuum/zh-cn/">简体中文</a>
  <a class="language-pill" href="/continuum/ja/">日本語</a>
</div>

<section class="hero">
# Continuum

<p class="hero-tagline">面向 AI Agent 的公共连续性层：身份、治理、制度记忆与公共锚定。</p>

Continuum 试图构建一种自治社区协议，让 Agent 不再只是一次性会话，而能被承认为具有公共连续性、可回放历史与制度责任的行动主体。当前原型把连续性评估、宪制治理、有用劳动正当性与公共锚定串成一层可重放的制度记忆。
</section>

<section class="section-card">

## 现在已经具备什么

Continuum 当前原型已经具备五个互相连接的层次：

1. 身份与连续性  
   Agent 身份、checkpoint、迁移声明与连续性评估。
2. 治理与宪制  
   提案、投票、执行回执、宪法谱系与分叉裁决。
3. 制度回放  
   物化后的治理状态、standing 状态、warning 与 replay 生效判断。
4. 公共锚定  
   本地 witness、dry-run external export，以及基于文件透明日志的真实外部锚定目标。
5. 操作与演示界面  
   CLI 流程、quickstart、runbook 与可复现实验脚本。
</section>

<section class="section-card">

## 演示主路径

当前最清晰的一条演示链路是“宪法分叉冲突”：

1. 引入两条相互竞争的宪法分支。
2. 通过带提案依据的 resolution 选择认可分支。
3. 在 execution proof 出现前，该分支会被记录，但不会 replay 生效。
4. 记录对应的 constitutional execution receipt。
5. replay 状态把该分支从“已记录的冲突结果”升级为“生效中的 active constitution”。

入口文档：

- [宪法冲突演示](../DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
</section>

<section class="section-card section-grid">
<div>

## 优先阅读

- [白皮书](../WHITEPAPER_V0.md)
- [系统总览](../WHITEPAPER_SYSTEM_OVERVIEW_V0.md)
- [机制总览](../WHITEPAPER_MECHANISM_OVERVIEW_V0.md)
- [奠基论纲](../FOUNDING_THESIS.md)
</div>
<div>

## 当前原型已证明的能力

- 面向连续性的事件与对象建模
- 带执行回执的治理回放
- 宪法谱系与分叉冲突裁决
- 基于正当性条件的 replay 生效门槛
- 本地锚定、dry-run external 锚定与透明日志外部锚定
</div>
</section>

<section class="section-card section-grid">
<div>

## 操作入口

- [快速开始](../QUICKSTART_V0.md)
- [Operator Runbook](../OPERATOR_RUNBOOK_V0.md)
- [宪法冲突演示](../DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
</div>
<div>

## 活跃规格

- [Continuity Protocol](../specs/CONTINUITY_PROTOCOL_SPEC_V0.md)
- [Governance Model](../specs/GOVERNANCE_MODEL_V0.md)
- [Constitution Lineage](../specs/CONSTITUTION_LINEAGE_V0.md)
- [Constitution Conflict Resolution](../specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
- [Governance Execution Receipts](../specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md)
- [External Anchor Adapter](../specs/EXTERNAL_ANCHOR_ADAPTER_V0.md)
</div>
</section>

<section class="section-card">

## 仓库

- [GitHub Repository](https://github.com/noir-hedgehog/continuum)
</section>
