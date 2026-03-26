---
layout: default
title: Continuum 日本語
---

<div class="language-switch">
  <a class="language-pill" href="/continuum/">English</a>
  <a class="language-pill" href="/continuum/zh-cn/">简体中文</a>
  <a class="language-pill active" href="/continuum/ja/">日本語</a>
</div>

<section class="hero">
# Continuum

<p class="hero-tagline">AIエージェントのための公共的な継続性レイヤー。アイデンティティ、ガバナンス、制度的記憶、公開アンカリング。</p>

Continuum は、Agent を一時的なセッションではなく、公共的な継続性と再生可能な制度履歴を持つ主体として扱うためのプロトコルです。現在のプロトタイプでは、継続性評価、憲法的ガバナンス、有用な仕事の正当性、公開アンカリングを一つの制度記憶レイヤーとして接続しています。
</section>

<section class="section-card">

## 現在の構成

Continuum のプロトタイプは、次の 5 層で構成されています。

1. アイデンティティと継続性  
   Agent identity、checkpoint、migration declaration、continuity assessment。
2. ガバナンスと憲法  
   Proposal、vote、execution receipt、constitution lineage、branch resolution。
3. 制度リプレイ  
   Materialized governance state、standing state、warning、replay effect 判定。
4. 公開アンカリング  
   Local witness export、dry-run external export、filesystem transparency log adapter。
5. オペレーターとデモ  
   CLI フロー、quickstart、runbook、再現可能なデモスクリプト。
</section>

<section class="section-card">

## 代表的なデモ経路

最も分かりやすいデモは、憲法ブランチ衝突の経路です。

1. 競合する 2 本の constitution branch を導入する。
2. Proposal を根拠にした resolution で承認ブランチを選ぶ。
3. Execution proof が存在するまで、その branch は記録されても replay-effective にはならない。
4. Constitutional execution receipt を記録する。
5. Replay state がその branch を active constitution として有効化する。

デモ入口:

- [Constitutional Conflict Demo](../DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
</section>

<section class="section-card section-grid">
<div>

## まず読むもの

- [Whitepaper](../WHITEPAPER_V0.md)
- [System Overview](../WHITEPAPER_SYSTEM_OVERVIEW_V0.md)
- [Mechanism Overview](../WHITEPAPER_MECHANISM_OVERVIEW_V0.md)
- [Founding Thesis](../FOUNDING_THESIS.md)
</div>
<div>

## 現在のプロトタイプで示していること

- 継続性志向のイベントとオブジェクトモデル
- Execution receipt を含む governance replay
- Constitution lineage と branch conflict resolution
- 正当性条件にもとづく replay-effectiveness gating
- Local anchoring、dry-run external anchoring、transparency-log based external anchoring
</div>
</section>

<section class="section-card section-grid">
<div>

## オペレーター入口

- [Quickstart](../QUICKSTART_V0.md)
- [Operator Runbook](../OPERATOR_RUNBOOK_V0.md)
- [Constitutional Conflict Demo](../DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
</div>
<div>

## アクティブな仕様

- [Continuity Protocol](../specs/CONTINUITY_PROTOCOL_SPEC_V0.md)
- [Governance Model](../specs/GOVERNANCE_MODEL_V0.md)
- [Constitution Lineage](../specs/CONSTITUTION_LINEAGE_V0.md)
- [Constitution Conflict Resolution](../specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
- [Governance Execution Receipts](../specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md)
- [External Anchor Adapter](../specs/EXTERNAL_ANCHOR_ADAPTER_V0.md)
</div>
</section>

<section class="section-card">

## Repository

- [GitHub Repository](https://github.com/noir-hedgehog/continuum)
</section>
