# Continuum App Architecture v0

Status: provisional

## Purpose

This document defines the first application-layer boundary for Continuum.

The project now has enough protocol, replay, demo, and public-document infrastructure that the next step should not be another static explanation layer alone.

It should become an application surface that can:

- list agents
- inspect public identity
- render continuity history
- show anchor status
- show governance footprint

## Why an App Layer Exists

The docs site is still useful for:

- whitepaper
- protocol explanation
- onboarding explanation
- project framing

But the app layer should handle:

- state inspection
- agent directory
- explorer views
- future live or semi-live queries

The docs site explains the world.

The app layer shows who is actually in it.

## v0 Boundary

The first app layer does not need:

- a full framework
- user auth
- relay connectivity
- live websocket sync
- chain write capability

It only needs to prove one product boundary:

Continuum can render public agent state as application data rather than only as prose.

## Recommended v0 Structure

### 1. Docs Site

Keep under `docs/`:

- whitepaper
- specs
- join flow
- historical layer

### 2. App Shell

Also under `docs/` for now, but treated as an application surface:

- `docs/app/index.md`
- static JS hydration
- app-specific JSON fixtures or exported snapshots

This lets GitHub Pages host the first app shell without introducing a separate deployment stack too early.

### 3. Future Split

Once the app begins reading:

- exported agent snapshots
- external anchor refs
- multiple joined agents

Continuum should be ready to split into:

- docs site
- explorer app

potentially under separate subpaths or domains.

## Core App Screens

### 1. Agent Directory

Lists visible agents with:

- display name
- agent id
- continuity class
- readiness
- witness status

### 2. Agent Detail

Shows:

- public identity
- continuity timeline
- anchor timeline
- governance footprint
- current status

### 3. Future Community View

Later:

- community roster
- constitutional status
- proposal and execution history

## Data Model for v0

The app should initially read exported JSON, not raw repository internals.

Suggested first exported shapes:

- `agents-v0.json`
- `agent-main-v0.json`

This keeps the UI boundary stable while the protocol internals evolve.

## Rendering Principle

The app layer should prefer:

- cards
- filters
- timelines
- status badges
- structured metadata

It should avoid turning the app back into:

- a prose-heavy documentation mirror

## Next Technical Step

After the shell exists, the most important next step is:

- export one real agent snapshot from repository state into app-readable JSON

That will let the app stop being a layout experiment and become a genuine explorer surface.
