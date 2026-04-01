---
layout: default
title: Continuum Playground
---

<div class="language-switch" markdown="1">
  <a class="language-pill active" href="/continuum/playground/">Playground</a>
  <a class="language-pill" href="/continuum/">Home</a>
  <a class="language-pill" href="/continuum/zh-cn/">简体中文</a>
</div>

<section class="hero" markdown="1">
# Continuum Playground

<p class="hero-tagline">A visual walkthrough of constitutional conflict, legitimacy, and replay effectiveness.</p>

This playground turns the current strongest Continuum demo path into an inspectable state machine. It is static and local to GitHub Pages, but it mirrors the protocol logic already implemented in the repository prototype.
</section>

<div class="playground-layout">
  <section class="section-card playground-sidebar">
    <h2>Scenario</h2>
    <p id="scenario-summary">Loading scenario...</p>

    <div class="playground-steps" id="playground-steps"></div>
  </section>

  <section class="section-card playground-main">
    <div class="playground-stage">
      <div>
        <p class="playground-label">Current Stage</p>
        <h2 id="stage-title">Root constitution</h2>
        <p id="stage-summary">The community starts from a single recognized constitution. There is no institutional ambiguity yet.</p>
      </div>
      <div class="playground-badges" id="stage-badges"></div>
    </div>

    <div class="playground-grid">
      <div class="playground-panel">
        <h3>Institutional State</h3>
        <ul id="state-list"></ul>
      </div>
      <div class="playground-panel">
        <h3>Why It Matters</h3>
        <p id="stage-meaning"></p>
      </div>
    </div>

    <div class="playground-grid">
      <div class="playground-panel">
        <h3>Warnings</h3>
        <ul id="warning-list"></ul>
      </div>
      <div class="playground-panel">
        <h3>Replay Snapshot</h3>
        <pre id="state-json" class="playground-json"></pre>
      </div>
    </div>
  </section>
</div>

<section class="section-card" markdown="1">
## Related Docs

- [Constitutional Conflict Demo](../DEMO_CONSTITUTIONAL_CONFLICT_V0.md)
- [Constitution Conflict Resolution Spec](../specs/CONSTITUTION_CONFLICT_RESOLUTION_V0.md)
- [Constitution Lineage Spec](../specs/CONSTITUTION_LINEAGE_V0.md)
- [Governance Execution Receipts](../specs/GOVERNANCE_EXECUTION_RECEIPTS_V0.md)
</section>

<script>
const SCENARIO_PATH = "/continuum/playground/scenarios/constitutional-conflict-v0.json";

let PLAYGROUND_STAGES = [];
let stepButtons = [];
const scenarioSummaryEl = document.getElementById("scenario-summary");
const stepContainerEl = document.getElementById("playground-steps");
const titleEl = document.getElementById("stage-title");
const summaryEl = document.getElementById("stage-summary");
const badgesEl = document.getElementById("stage-badges");
const stateListEl = document.getElementById("state-list");
const warningListEl = document.getElementById("warning-list");
const meaningEl = document.getElementById("stage-meaning");
const stateJsonEl = document.getElementById("state-json");

function renderStage(index) {
  const stage = PLAYGROUND_STAGES[index];
  titleEl.textContent = stage.title;
  summaryEl.textContent = stage.summary;
  meaningEl.textContent = stage.meaning;
  badgesEl.innerHTML = stage.badges.map((badge) => `<span class="playground-badge">${badge}</span>`).join("");
  stateListEl.innerHTML = stage.stateList.map((item) => `<li>${item}</li>`).join("");
  warningListEl.innerHTML = stage.warnings.length
    ? stage.warnings.map((item) => `<li>${item}</li>`).join("")
    : "<li>No active warnings.</li>";
  stateJsonEl.textContent = JSON.stringify(stage.snapshot, null, 2);

  stepButtons.forEach((button, buttonIndex) => {
    button.classList.toggle("active", buttonIndex === index);
  });
}

function installScenario(scenario) {
  PLAYGROUND_STAGES = scenario.stages.map((stage) => ({
    title: stage.title,
    summary: stage.summary,
    badges: stage.badges,
    stateList: stage.state_list,
    meaning: stage.meaning,
    warnings: stage.warnings,
    snapshot: stage.snapshot
  }));

  scenarioSummaryEl.textContent = scenario.summary;
  stepContainerEl.innerHTML = scenario.stages
    .map(
      (stage, index) =>
        `<button class="playground-step${index === 0 ? " active" : ""}" data-step="${index}">${stage.button_label}</button>`
    )
    .join("");

  stepButtons = Array.from(document.querySelectorAll(".playground-step"));
  stepButtons.forEach((button, index) => {
    button.addEventListener("click", () => renderStage(index));
  });

  renderStage(0);
}

fetch(SCENARIO_PATH)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`Failed to load scenario: ${response.status}`);
    }
    return response.json();
  })
  .then((scenario) => installScenario(scenario))
  .catch((error) => {
    scenarioSummaryEl.textContent = "Scenario fixture failed to load.";
    titleEl.textContent = "Playground load error";
    summaryEl.textContent = error.message;
    meaningEl.textContent =
      "The visual playground now expects a scenario fixture. Once the JSON is available, the page will hydrate from repository data instead of hard-coded stage objects.";
    warningListEl.innerHTML = "<li>fixture_load_failed</li>";
    stateListEl.innerHTML = "<li>scenario_fixture: unavailable</li>";
    stateJsonEl.textContent = JSON.stringify({ error: error.message, path: SCENARIO_PATH }, null, 2);
  });
</script>
