#!/bin/zsh
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

cd "$ROOT"

agent_dir="$ROOT/.continuum/agents"
mkdir -p "$agent_dir"

ensure_role() {
  local name="$1"
  local display_name="$2"
  local description="$3"
  local agent_path="$agent_dir/role__continuum__${name}.json"

  if [[ -f "$agent_path" ]]; then
    echo "Exists: role:continuum:${name}"
    return 0
  fi

  PYTHONPATH="$ROOT" python3 -m src.cli.main role init \
    --scope continuum \
    --name "$name" \
    --display-name "$display_name" \
    --description "$description" \
    --operator-disclosure "Public automation role (operator and model sessions may vary)." >/dev/null

  if [[ -f "$agent_path" ]]; then
    echo "Created: role:continuum:${name}"
  else
    echo "Error: expected $agent_path to be created" >&2
    return 1
  fi
}

ensure_role "main-integrator" "Continuum Main Integrator" "Keep the repository coherent across roadmap, docs, runtime, demos, and public surfaces."
ensure_role "builder" "Continuum Builder" "Advance executable runtime, CLI, tests, demos, and export paths."
ensure_role "witness-operator" "Continuum Witness Operator" "Turn repository state into public evidence: exports, snapshots, and verification notes."
ensure_role "protocol-steward" "Continuum Protocol Steward" "Keep continuity, governance, object model, and assessment semantics internally consistent."
ensure_role "validation-scout" "Continuum Validation Scout" "Produce validation briefs, objection logs, and positioning recommendations grounded in founder notes."

