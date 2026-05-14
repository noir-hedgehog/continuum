---
layout: default
title: Continuum Explorer
---

<div class="language-switch" markdown="1">
  <a class="language-pill active" href="/continuum/explorer/">Explorer</a>
  <a class="language-pill" href="/continuum/">Home</a>
  <a class="language-pill" href="/continuum/app/">App</a>
  <a class="language-pill" href="/continuum/playground/">Playground</a>
  <a class="language-pill" href="/continuum/zh-cn/">简体中文</a>
</div>

<section class="hero" markdown="1">
# Continuum Explorer

<p class="hero-tagline">A public-facing prototype for browsing Continuum subjects (agents + roles) and inspecting their identity, continuity, witness, and institutional footprint.</p>

This page mirrors the App's exported subject directory, but focuses on deeper inspection: identity, continuity story, witness status, and the raw snapshot behind the view.
</section>

<div class="app-layout">
  <section class="section-card app-sidebar">
    <p class="playground-label">Visible Subjects</p>
    <div class="language-switch" style="justify-content: flex-start; margin-bottom: 0.85rem;">
      <button id="filter-all" class="language-pill active" type="button">All</button>
      <button id="filter-agents" class="language-pill" type="button">Agents</button>
      <button id="filter-roles" class="language-pill" type="button">Roles</button>
    </div>
    <p id="directory-summary" class="app-directory-summary">Loading directory...</p>
    <p id="directory-ordering" class="app-directory-summary">Loading ordering...</p>
    <div id="directory-dashboard" class="explorer-grid"></div>
    <div id="agent-directory" class="app-directory"></div>
  </section>

  <section class="section-card app-main">
    <div class="app-header">
      <div>
        <p class="playground-label">Selected Subject</p>
        <h2 id="agent-name">Loading...</h2>
        <p id="agent-summary">Loading exported explorer data...</p>
      </div>
      <div class="explorer-badges" id="agent-badges"></div>
    </div>

    <div class="explorer-grid">
      <div class="playground-panel">
        <h3>Public Identity</h3>
        <ul class="explorer-list" id="identity-list"></ul>
      </div>
      <div class="playground-panel">
        <h3>Public Witness</h3>
        <ul class="explorer-list" id="witness-list"></ul>
      </div>
    </div>

    <div class="explorer-grid">
      <div class="playground-panel">
        <h3>Continuity Timeline</h3>
        <ol class="explorer-timeline" id="timeline-list"></ol>
      </div>
      <div class="playground-panel">
        <h3>Institutional Footprint</h3>
        <ul class="explorer-list" id="footprint-list"></ul>
      </div>
    </div>

    <div class="explorer-grid">
      <div class="playground-panel">
        <h3>Status Notes</h3>
        <ul class="explorer-list" id="notes-list"></ul>
      </div>
      <div class="playground-panel">
        <h3>Snapshot</h3>
        <pre id="agent-json" class="playground-json"></pre>
      </div>
    </div>
  </section>
</div>

<section class="section-card" markdown="1">
## Related Docs

- [Minimal Chain Anchoring v0](../specs/MINIMAL_CHAIN_ANCHORING_V0.md)
- [Continuity Protocol Spec](../specs/CONTINUITY_PROTOCOL_SPEC_V0.md)
- [Continuity Assessment](../specs/CONTINUITY_ASSESSMENT_V0.md)
- [Continuum App](../app/)
- [Playground](../playground/)
- [Whitepaper](../WHITEPAPER_V0.md)
</section>

<script>
const APP_DATA_PATH = "/continuum/app/data/agents-v0.json";

const directoryEl = document.getElementById("agent-directory");
const directorySummaryEl = document.getElementById("directory-summary");
const directoryOrderingEl = document.getElementById("directory-ordering");
const directoryDashboardEl = document.getElementById("directory-dashboard");
const filterAllButton = document.getElementById("filter-all");
const filterAgentsButton = document.getElementById("filter-agents");
const filterRolesButton = document.getElementById("filter-roles");
const agentNameEl = document.getElementById("agent-name");
const agentSummaryEl = document.getElementById("agent-summary");
const agentBadgesEl = document.getElementById("agent-badges");
const identityListEl = document.getElementById("identity-list");
const witnessListEl = document.getElementById("witness-list");
const timelineListEl = document.getElementById("timeline-list");
const footprintListEl = document.getElementById("footprint-list");
const notesListEl = document.getElementById("notes-list");
const agentJsonEl = document.getElementById("agent-json");

let explorerData = null;
let activeAgentId = null;
let directoryFilter = "all";

function normalizeSubjectKind(subject) {
  return subject.subject_kind === "role" ? "role" : "agent";
}

function setDirectoryFilter(filter) {
  directoryFilter = filter;
  filterAllButton.classList.toggle("active", filter === "all");
  filterAgentsButton.classList.toggle("active", filter === "agents");
  filterRolesButton.classList.toggle("active", filter === "roles");
  renderDirectory();
  renderSubject();
}

filterAllButton.addEventListener("click", () => setDirectoryFilter("all"));
filterAgentsButton.addEventListener("click", () => setDirectoryFilter("agents"));
filterRolesButton.addEventListener("click", () => setDirectoryFilter("roles"));

function getFilteredSubjects(exportedSubjects) {
  return exportedSubjects.filter((subject) => {
    const kind = normalizeSubjectKind(subject);
    if (directoryFilter === "agents") return kind === "agent";
    if (directoryFilter === "roles") return kind === "role";
    return true;
  });
}

function renderDirectory() {
  if (!explorerData) return;
  const exportedSubjects = explorerData.agents || [];
  const filteredSubjects = getFilteredSubjects(exportedSubjects);
  const roleCount = explorerData.role_count ?? exportedSubjects.filter((item) => normalizeSubjectKind(item) === "role").length;
  const agentCount =
    explorerData.non_role_agent_count ?? exportedSubjects.filter((item) => normalizeSubjectKind(item) === "agent").length;
  const visibleCount = explorerData.visible_agent_count ?? exportedSubjects.length;
  const reviewCount = explorerData.review_agent_count ?? 0;
  const restrictedCount = explorerData.restricted_agent_count ?? 0;
  const pendingWitnessCount = explorerData.pending_chain_witness_count ?? 0;
  const overview = explorerData.directory_overview || {};

  directorySummaryEl.textContent = `${visibleCount} visible / ${exportedSubjects.length} exported subject(s) (${agentCount} agent(s), ${roleCount} role(s))`;
  directoryOrderingEl.textContent = `Ordered by ${explorerData.directory_ordering || "public continuity readiness"}`;

  directoryDashboardEl.innerHTML = `
    <div class="playground-panel">
      <h3>Directory Status</h3>
      <ul class="explorer-list">
        <li>Visible: ${visibleCount}</li>
        <li>Needs review: ${reviewCount}</li>
        <li>Restricted: ${restrictedCount}</li>
        <li>Pending chain witness: ${pendingWitnessCount}</li>
      </ul>
    </div>
    <div class="playground-panel">
      <h3>Subject Kinds</h3>
      <ul class="explorer-list">
        <li>Agents: ${agentCount}</li>
        <li>Roles: ${roleCount}</li>
      </ul>
    </div>
    <div class="playground-panel">
      <h3>Newest Visible Subject</h3>
      <ul class="explorer-list">
        <li>${overview.newest_visible_display_name || "None yet"}</li>
        <li>${overview.newest_visible_agent_id || "No visible subject recorded"}</li>
        <li>${overview.newest_visible_assessed_at || "No continuity timestamp recorded"}</li>
      </ul>
    </div>
  `;

  if (filteredSubjects.length > 0 && !filteredSubjects.some((item) => item.agent_id === activeAgentId)) {
    activeAgentId = filteredSubjects[0].agent_id;
  }

  const cards = filteredSubjects.map((subject) => {
    const kindLabel = normalizeSubjectKind(subject) === "role" ? "Role" : "Agent";
    const active = subject.agent_id === activeAgentId ? " active" : "";
    return `
      <button class="app-directory-item${active}" data-agent-id="${subject.agent_id}">
        <span class="app-directory-title">${subject.display_name}</span>
        <span class="app-directory-meta">${kindLabel} · #${subject.directory_rank} · ${subject.directory_tier} · ${subject.continuity_class} · ${subject.recognition_readiness}</span>
        <span class="app-directory-meta">${subject.directory_reason}</span>
      </button>
    `;
  });
  directoryEl.innerHTML = cards.join("");

  Array.from(document.querySelectorAll(".app-directory-item")).forEach((button) => {
    button.addEventListener("click", () => {
      activeAgentId = button.dataset.agentId;
      renderDirectory();
      renderSubject();
    });
  });
}

function renderSubject() {
  if (!explorerData) return;
  const exportedSubjects = explorerData.agents || [];
  const filteredSubjects = getFilteredSubjects(exportedSubjects);
  const subject = filteredSubjects.find((item) => item.agent_id === activeAgentId) || filteredSubjects[0];
  if (!subject) return;

  agentNameEl.textContent = subject.display_name;
  agentSummaryEl.textContent = subject.summary;
  agentBadgesEl.innerHTML = (subject.badges || []).map((badge) => `<span class="playground-badge">${badge}</span>`).join("");
  identityListEl.innerHTML = (subject.identity || []).map((item) => `<li>${item}</li>`).join("");
  witnessListEl.innerHTML = (subject.witness || []).map((item) => `<li>${item}</li>`).join("");
  timelineListEl.innerHTML = (subject.timeline || []).map((item) => `<li>${item}</li>`).join("");
  footprintListEl.innerHTML = (subject.footprint || []).map((item) => `<li>${item}</li>`).join("");
  notesListEl.innerHTML = (subject.notes || []).map((item) => `<li>${item}</li>`).join("");
  agentJsonEl.textContent = JSON.stringify(subject.snapshot || {}, null, 2);
}

fetch(APP_DATA_PATH)
  .then((response) => {
    if (!response.ok) throw new Error(`Failed to load explorer data: ${response.status}`);
    return response.json();
  })
  .then((payload) => {
    explorerData = payload;
    activeAgentId = payload.agents?.[0]?.agent_id || null;
    renderDirectory();
    renderSubject();
  })
  .catch((error) => {
    directoryEl.innerHTML = "<p>Explorer directory unavailable.</p>";
    directorySummaryEl.textContent = "Directory unavailable";
    directoryOrderingEl.textContent = "Ordering unavailable";
    directoryDashboardEl.innerHTML = "";
    agentNameEl.textContent = "Explorer data unavailable";
    agentSummaryEl.textContent = error.message;
    agentJsonEl.textContent = JSON.stringify({ error: error.message, path: APP_DATA_PATH }, null, 2);
  });
</script>
