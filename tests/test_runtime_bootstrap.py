from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from src.anchors.export import AnchorExportRequest, DryRunExternalAnchorAdapter, LocalAnchorAdapter
from src.cli.main import main
from src.runtime.canonical import canonical_json
from src.runtime.events import build_checkpoint_payload, build_event, build_migration_payload
from src.runtime.store import RepositoryStore


class CanonicalRuntimeTests(unittest.TestCase):
    def test_canonical_json_sorts_keys(self) -> None:
        left = {"b": 1, "a": {"d": 2, "c": 3}}
        right = {"a": {"c": 3, "d": 2}, "b": 1}
        self.assertEqual(canonical_json(left), canonical_json(right))

    def test_event_id_is_deterministic_for_same_pre_sign_image(self) -> None:
        payload = build_checkpoint_payload(
            agent_id="agent:continuum:main",
            scope="session_handoff",
            summary="Checkpoint summary",
            checkpoint_id="checkpoint:continuum-main:0001",
        )
        first = build_event(
            kind="memory_checkpoint",
            actor_id="agent:continuum:main",
            signing_key="key:continuum:main",
            secret_hex="11" * 32,
            payload=payload,
            refs=[],
            created_at="2026-03-21T00:00:00Z",
            community_id="community:continuum:lab",
        )
        second = build_event(
            kind="memory_checkpoint",
            actor_id="agent:continuum:main",
            signing_key="key:continuum:main",
            secret_hex="11" * 32,
            payload=payload,
            refs=[],
            created_at="2026-03-21T00:00:00Z",
            community_id="community:continuum:lab",
        )
        self.assertEqual(first["event_id"], second["event_id"])
        self.assertEqual(first["signature"], second["signature"])

    def test_store_is_idempotent_for_same_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = RepositoryStore(Path(tmp))
            payload = build_migration_payload(
                agent_id="agent:continuum:main",
                migration_type="session_restart",
                from_ref="session:old",
                to_ref="session:new",
                reason="restart",
                evidence=["docs/TASK_BOARD.md"],
                expected_continuity_class="same_agent",
                effective_at="2026-03-21T00:00:00Z",
                migration_id="migration:continuum-main:0001",
            )
            event = build_event(
                kind="migration_declare",
                actor_id="agent:continuum:main",
                signing_key="key:continuum:main",
                secret_hex="22" * 32,
                payload=payload,
                refs=[],
                created_at="2026-03-21T00:00:01Z",
            )
            first_path = store.save_event(event)
            second_path = store.save_event(event)
            self.assertEqual(first_path, second_path)
            self.assertEqual(store.load_event(event["event_id"])["event_id"], event["event_id"])

    def test_local_anchor_adapter_records_confirmed_local_witness(self) -> None:
        adapter = LocalAnchorAdapter()
        record = adapter.export(
            AnchorExportRequest(
                anchor_type="governance_state_root",
                subject_ref="community:continuum:lab",
                root_hash="state:test",
                anchored_at="2026-03-22T00:00:00Z",
            )
        )
        self.assertEqual(record["anchor_target"], "adapter:local_witness_v0")
        self.assertEqual(record["anchor_status"], "confirmed_external")
        self.assertNotIn("external_reference", record)

    def test_dry_run_external_adapter_exposes_external_shape(self) -> None:
        adapter = DryRunExternalAnchorAdapter()
        record = adapter.export(
            AnchorExportRequest(
                anchor_type="continuity_assessment_root",
                subject_ref="assessment:test",
                root_hash="state:test",
                anchored_at="2026-03-22T00:00:00Z",
            )
        )
        self.assertEqual(record["anchor_target"], "adapter:dry_run_external_v0")
        self.assertEqual(record["anchor_status"], "submitted_external")
        self.assertIn("external_reference", record)
        self.assertEqual(record["target_metadata"]["submission_mode"], "dry_run")


class CliBootstrapTests(unittest.TestCase):
    def run_cli(self, args: list[str]) -> tuple[int, dict]:
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = main(args)
        rendered = buffer.getvalue().strip()
        payload = json.loads(rendered) if rendered else {}
        return code, payload

    def test_cli_end_to_end_bootstrap_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                Path(tmp).mkdir(parents=True, exist_ok=True)
                os.chdir(tmp)
                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            "main",
                            "--display-name",
                            "Continuum Main",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "profile",
                            "set",
                            "--display-name",
                            "Continuum Main",
                            "--description",
                            "Bootstrap agent",
                            "--artifact-ref",
                            "docs/FOUNDING_THESIS.md",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "memory",
                            "checkpoint",
                            "create",
                            "--scope",
                            "session_handoff",
                            "--summary",
                            "Repository reconstruction and bootstrap implementation",
                            "--artifact-ref",
                            "docs/TASK_BOARD.md",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "migration",
                            "declare",
                            "--migration-type",
                            "session_restart",
                            "--from-ref",
                            "session:continuum:run-old",
                            "--to-ref",
                            "session:continuum:run-new",
                            "--reason",
                            "Automation restart",
                            "--evidence",
                            "docs/REVISION_LOG.md",
                        ]
                    )[0],
                    0,
                )
                events = sorted((Path(tmp) / ".continuum" / "events").glob("*.json"))
                self.assertEqual(len(events), 3)
                rendered = json.loads(events[-1].read_text(encoding="utf-8"))
                self.assertIn(rendered["kind"], {"agent_profile", "memory_checkpoint", "migration_declare"})
            finally:
                os.chdir(cwd)

    def test_query_commands_materialize_deterministic_agent_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Main",
                        "--description",
                        "Bootstrap agent",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Checkpoint one",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "task_memory",
                        "--summary",
                        "Checkpoint two",
                    ]
                )
                self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "session_restart",
                        "--from-ref",
                        "session:continuum:run-old",
                        "--to-ref",
                        "session:continuum:run-new",
                        "--reason",
                        "Automation restart",
                    ]
                )

                first_code, first_state = self.run_cli(["query", "agent-state", "--refresh"])
                second_code, second_state = self.run_cli(["query", "agent-state"])
                self.assertEqual(first_code, 0)
                self.assertEqual(second_code, 0)
                self.assertEqual(first_state["state_root"], second_state["state_root"])
                self.assertEqual(first_state["event_count"], 4)
                self.assertEqual(first_state["latest_profile"]["display_name"], "Continuum Main")
                self.assertEqual(first_state["latest_checkpoint_by_scope"]["task_memory"]["scope"], "task_memory")

                history_code, history = self.run_cli(["query", "agent-history"])
                self.assertEqual(history_code, 0)
                self.assertEqual(len(history["agent_history"]), 4)

                checkpoint_code, checkpoints = self.run_cli(
                    ["query", "checkpoint-lineage", "--scope", "session_handoff"]
                )
                self.assertEqual(checkpoint_code, 0)
                self.assertEqual(len(checkpoints["checkpoint_lineage"]), 1)

                migration_code, migrations = self.run_cli(
                    ["query", "migration-lineage", "--migration-type", "session_restart"]
                )
                self.assertEqual(migration_code, 0)
                self.assertEqual(len(migrations["migration_lineage"]), 1)

                derived_state_path = Path(tmp) / ".continuum" / "state" / "agents" / "agent__continuum__main.json"
                self.assertTrue(derived_state_path.exists())
            finally:
                os.chdir(cwd)

    def test_agent_use_supports_multi_actor_cross_community_standing_isolation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            "main",
                            "--display-name",
                            "Continuum Main",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "profile",
                            "set",
                            "--display-name",
                            "Continuum Main",
                            "--description",
                            "Primary actor",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            "reviewer",
                            "--display-name",
                            "Continuum Reviewer",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "profile",
                            "set",
                            "--display-name",
                            "Continuum Reviewer",
                            "--description",
                            "Review actor",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(["agent", "use", "--agent-id", "agent:continuum:main"])[0],
                    0,
                )

                for community_id in ("community:continuum:lab", "community:continuum:guild"):
                    self.assertEqual(
                        self.run_cli(
                            [
                                "governance",
                                "membership",
                                "grant",
                                "--community-id",
                                community_id,
                                "--member-agent-id",
                                "agent:continuum:main",
                            ]
                        )[0],
                        0,
                    )
                self.assertEqual(
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            "community:continuum:lab",
                            "--member-agent-id",
                            "agent:continuum:reviewer",
                            "--role",
                            "reviewer",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(["agent", "use", "--agent-id", "agent:continuum:reviewer"])[0],
                    0,
                )

                self.assertEqual(
                    self.run_cli(
                        [
                            "continuity",
                            "case",
                            "open",
                            "--community-id",
                            "community:continuum:lab",
                            "--subject-agent-id",
                            "agent:continuum:main",
                            "--trigger-type",
                            "branch_conflict",
                            "--linked-ref",
                            "migration:continuum-main:branch",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(["agent", "use", "--agent-id", "agent:continuum:main"])[0],
                    0,
                )

                lab_standing_code, lab_standing = self.run_cli(
                    [
                        "query",
                        "standing-state",
                        "--subject-agent-id",
                        "agent:continuum:main",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                    ]
                )
                self.assertEqual(lab_standing_code, 0)
                self.assertEqual(lab_standing["current_standing"], "restricted")

                guild_standing_code, guild_standing = self.run_cli(
                    [
                        "query",
                        "standing-state",
                        "--subject-agent-id",
                        "agent:continuum:main",
                        "--community-id",
                        "community:continuum:guild",
                        "--refresh",
                    ]
                )
                self.assertEqual(guild_standing_code, 0)
                self.assertEqual(guild_standing["current_standing"], "clear")

                blocked_code, blocked_payload = self.run_cli(
                    [
                        "governance",
                        "proposal",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-type",
                        "constitutional",
                        "--title",
                        "Blocked in lab",
                        "--summary",
                        "Restricted standing should prevent this proposal.",
                    ]
                )
                self.assertEqual(blocked_code, 2)
                self.assertEqual(blocked_payload, {})

                guild_proposal_code, guild_proposal = self.run_cli(
                    [
                        "governance",
                        "proposal",
                        "submit",
                        "--community-id",
                        "community:continuum:guild",
                        "--proposal-type",
                        "constitutional",
                        "--title",
                        "Allowed in guild",
                        "--summary",
                        "Clear standing in guild should permit this proposal.",
                    ]
                )
                self.assertEqual(guild_proposal_code, 0)
                self.assertEqual(guild_proposal["payload"]["proposal"]["community_id"], "community:continuum:guild")

                _, lab_anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "standing_state_root",
                        "--subject-agent-id",
                        "agent:continuum:main",
                        "--community-id",
                        "community:continuum:lab",
                        "--anchored-at",
                        "2026-03-21T12:00:00Z",
                    ]
                )
                _, guild_anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "standing_state_root",
                        "--subject-agent-id",
                        "agent:continuum:main",
                        "--community-id",
                        "community:continuum:guild",
                        "--anchored-at",
                        "2026-03-21T12:05:00Z",
                    ]
                )
                self.assertNotEqual(lab_anchor["subject_ref"], guild_anchor["subject_ref"])
                self.assertNotEqual(lab_anchor["root_hash"], guild_anchor["root_hash"])
            finally:
                os.chdir(cwd)

    def test_continuity_assessment_defaults_to_same_agent_for_repo_restart(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                        "--operator-disclosure",
                        "founder-supervised",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Main",
                        "--description",
                        "Bootstrap agent",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Checkpoint one",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "session_restart",
                        "--from-ref",
                        "session:continuum:run-old",
                        "--to-ref",
                        "session:continuum:run-new",
                        "--reason",
                        "Automation restart",
                    ]
                )

                code, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.assertEqual(code, 0)
                self.assertEqual(assessment["assessed_by_agent_id"], "agent:continuum:main")
                self.assertEqual(assessment["continuity_class"], "same_agent")
                self.assertEqual(assessment["confidence_band"], "high")
                self.assertEqual(assessment["recognition_readiness"], "ready")
                self.assertEqual(assessment["canonical_branch_status"], "canonical")
                self.assertIn("session_restart_declared", assessment["supporting_evidence"])
                assessment_path = (
                    Path(tmp)
                    / ".continuum"
                    / "state"
                    / "assessments"
                    / f"{assessment['assessment_id'].replace(':', '__')}.json"
                )
                self.assertTrue(assessment_path.exists())
            finally:
                os.chdir(cwd)

    def test_continuity_assessment_downgrades_operator_change_to_successor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Main",
                        "--description",
                        "Bootstrap agent",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Checkpoint one",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Declared handoff",
                    ]
                )

                code, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.assertEqual(code, 0)
                self.assertEqual(assessment["continuity_class"], "successor_agent")
                self.assertEqual(assessment["recognition_readiness"], "needs_review")
                self.assertIn("strict_identity_preservation_not_met", assessment["blocking_issues"])
            finally:
                os.chdir(cwd)

    def test_continuity_case_open_derives_review_restrictions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "subject",
                        "--display-name",
                        "Continuum Subject",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "reviewer",
                        "--display-name",
                        "Continuum Reviewer",
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:reviewer"])
                self.run_cli(["governance", "constitution", "set", "--community-id", "community:continuum:lab"])
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:reviewer",
                        "--role",
                        "reviewer",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )
                code, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "branch_conflict",
                        "--linked-ref",
                        "migration:continuum-main:branch",
                    ]
                )
                self.assertEqual(code, 0)
                case = case_event["payload"]["continuity_case"]
                self.assertEqual(case["standing_during_review"], "restricted")
                self.assertEqual(case["status"], "opened")
                self.assertIn("block_treasury_execution", case["temporary_restrictions"])
                self.assertIn("block_canonical_role_claims", case["temporary_restrictions"])

                standing_code, standing = self.run_cli(
                    [
                        "query",
                        "standing-state",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                    ]
                )
                self.assertEqual(standing_code, 0)
                self.assertEqual(standing["current_standing"], "restricted")
                self.assertEqual(len(standing["open_cases"]), 1)
                self.assertIn("block_constitutional_voting", standing["active_restrictions"])
            finally:
                os.chdir(cwd)

    def test_continuity_case_decision_derives_standing_from_assessment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "subject",
                        "--display-name",
                        "Continuum Subject",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "gatekeeper",
                        "--display-name",
                        "Continuum Gatekeeper",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "decider",
                        "--display-name",
                        "Continuum Decider",
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:subject"])
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Subject",
                        "--description",
                        "Bootstrap agent",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Checkpoint one",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Declared handoff",
                    ]
                )
                _, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.assertEqual(assessment["assessed_by_agent_id"], "agent:continuum:subject")
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                self.run_cli(["governance", "constitution", "set", "--community-id", "community:continuum:lab"])
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:gatekeeper",
                        "--role",
                        "reviewer",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:decider",
                        "--role",
                        "reviewer",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )
                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "operator_handoff",
                        "--assessment-ref",
                        assessment["assessment_id"],
                        "--linked-ref",
                        migration["event_id"],
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:decider"])

                code, decision_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        assessment["assessment_id"],
                        "--reason",
                        "Successor keeps obligations but not sensitive powers",
                    ]
                )
                self.assertEqual(code, 0)
                decision = decision_event["payload"]["standing_decision"]
                self.assertEqual(decision["standing_after"], "restricted")
                self.assertEqual(decision["continuity_class"], "successor_agent")
                self.assertIn("treasury_execution", decision["rights_restricted"])
                self.assertIn("historical_accountability", decision["obligations_preserved"])

                standing_code, standing = self.run_cli(
                    [
                        "query",
                        "standing-state",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                    ]
                )
                self.assertEqual(standing_code, 0)
                self.assertEqual(standing["current_standing"], "restricted")
                self.assertEqual(standing["latest_decision"]["decision_id"], decision["decision_id"])
                self.assertEqual(standing["open_cases"], [])
            finally:
                os.chdir(cwd)

    def test_continuity_case_respects_assigned_assessor_and_decider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                for name in ("subject", "gatekeeper", "assessor", "decider", "outsider"):
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            name,
                            "--display-name",
                            f"Continuum {name.title()}",
                        ]
                    )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:subject"])
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Subject",
                        "--description",
                        "Subject under review",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Subject continuity checkpoint",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Authority handoff requiring review",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor"])
                _, assigned_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.assertEqual(assigned_assessment["assessed_by_agent_id"], "agent:continuum:assessor")

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:outsider"])
                _, outsider_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.assertEqual(outsider_assessment["assessed_by_agent_id"], "agent:continuum:outsider")

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                self.run_cli(["governance", "constitution", "set", "--community-id", "community:continuum:lab"])
                for reviewer in ("gatekeeper", "assessor", "decider", "outsider"):
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            "community:continuum:lab",
                            "--member-agent-id",
                            f"agent:continuum:{reviewer}",
                            "--role",
                            "reviewer",
                        ]
                    )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )

                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "operator_handoff",
                        "--assessment-ref",
                        assigned_assessment["assessment_id"],
                        "--assessment-ref",
                        outsider_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor",
                        "--decider-agent-id",
                        "agent:continuum:decider",
                        "--linked-ref",
                        migration["event_id"],
                    ]
                )
                case = case_event["payload"]["continuity_case"]
                self.assertEqual(case["assigned_assessor_agent_ids"], ["agent:continuum:assessor"])
                self.assertEqual(case["assigned_decider_agent_ids"], ["agent:continuum:decider"])

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:outsider"])
                outsider_decider_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        assigned_assessment["assessment_id"],
                        "--reason",
                        "Unassigned reviewer should not decide",
                    ]
                )
                self.assertEqual(outsider_decider_code, 2)

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:decider"])
                wrong_assessor_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        outsider_assessment["assessment_id"],
                        "--reason",
                        "Assessment from unassigned reviewer should not authorize a decision",
                    ]
                )
                self.assertEqual(wrong_assessor_code, 2)

                success_code, decision_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        assigned_assessment["assessment_id"],
                        "--reason",
                        "Assigned reviewer assessment supports successor standing",
                    ]
                )
                self.assertEqual(success_code, 0)
                self.assertEqual(
                    decision_event["payload"]["standing_decision"]["decided_by"],
                    "agent:continuum:decider",
                )
            finally:
                os.chdir(cwd)

    def test_continuity_case_decision_enforces_assessment_quorum_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                for name in ("subject", "gatekeeper", "assessor-a", "assessor-b", "decider"):
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            name,
                            "--display-name",
                            f"Continuum {name.title()}",
                        ]
                    )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:subject"])
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Subject",
                        "--description",
                        "Subject under quorum review",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Subject continuity checkpoint",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Authority handoff requiring quorum review",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor-a"])
                _, first_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor-b"])
                _, second_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                continuity_policies = {
                    "case_open": {
                        "allowed_standings": ["clear"],
                        "required_roles": ["maintainer", "reviewer"],
                        "allow_subject_self_open": False,
                    },
                    "case_decide": {
                        "allowed_standings": ["clear"],
                        "required_roles": ["maintainer", "reviewer"],
                        "allow_subject_self_decide": False,
                        "allow_opener_as_decider": False,
                        "min_assessment_count": 2,
                        "require_distinct_assessors": True,
                    },
                }

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--continuity-policies-json",
                        json.dumps(continuity_policies, sort_keys=True),
                    ]
                )
                for reviewer in ("gatekeeper", "assessor-a", "assessor-b", "decider"):
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            "community:continuum:lab",
                            "--member-agent-id",
                            f"agent:continuum:{reviewer}",
                            "--role",
                            "reviewer",
                        ]
                    )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )

                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "operator_handoff",
                        "--assessment-ref",
                        first_assessment["assessment_id"],
                        "--assessment-ref",
                        second_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor-a",
                        "--assessor-agent-id",
                        "agent:continuum:assessor-b",
                        "--decider-agent-id",
                        "agent:continuum:decider",
                        "--linked-ref",
                        migration["event_id"],
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:decider"])
                insufficient_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        first_assessment["assessment_id"],
                        "--reason",
                        "One assessment should not satisfy quorum",
                    ]
                )
                self.assertEqual(insufficient_code, 2)

                success_code, decision_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        first_assessment["assessment_id"],
                        "--assessment-id",
                        second_assessment["assessment_id"],
                        "--reason",
                        "Two assigned assessors satisfy quorum",
                    ]
                )
                self.assertEqual(success_code, 0)
                self.assertEqual(
                    decision_event["payload"]["standing_decision"]["assessment_refs"],
                    sorted([first_assessment["assessment_id"], second_assessment["assessment_id"]]),
                )
            finally:
                os.chdir(cwd)

    def test_continuity_case_reassignment_updates_current_reviewer_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                for name in ("subject", "gatekeeper", "assessor-a", "assessor-b", "decider-a", "decider-b"):
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            name,
                            "--display-name",
                            f"Continuum {name.title()}",
                        ]
                    )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:subject"])
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Subject",
                        "--description",
                        "Subject under reassigned review",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Subject continuity checkpoint",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Authority handoff requiring reassignment",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor-a"])
                _, first_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                self.run_cli(["governance", "constitution", "set", "--community-id", "community:continuum:lab"])
                for reviewer in (
                    "gatekeeper",
                    "assessor-a",
                    "assessor-b",
                    "decider-a",
                    "decider-b",
                ):
                    role = "maintainer" if reviewer == "gatekeeper" else "reviewer"
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            "community:continuum:lab",
                            "--member-agent-id",
                            f"agent:continuum:{reviewer}",
                            "--role",
                            role,
                        ]
                    )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )

                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "operator_handoff",
                        "--assessment-ref",
                        first_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor-a",
                        "--decider-agent-id",
                        "agent:continuum:decider-a",
                        "--linked-ref",
                        migration["event_id"],
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor-b"])
                _, second_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                reassign_code, reassign_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "reassign",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-ref",
                        second_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor-b",
                        "--decider-agent-id",
                        "agent:continuum:decider-b",
                        "--reason",
                        "Original reviewers unavailable after handoff",
                    ]
                )
                self.assertEqual(reassign_code, 0)
                assignment = reassign_event["payload"]["case_assignment"]
                self.assertEqual(assignment["required_assessment_refs"], [second_assessment["assessment_id"]])
                self.assertEqual(assignment["assigned_assessor_agent_ids"], ["agent:continuum:assessor-b"])
                self.assertEqual(assignment["assigned_decider_agent_ids"], ["agent:continuum:decider-b"])

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:decider-a"])
                stale_decider_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        first_assessment["assessment_id"],
                        "--reason",
                        "Stale decider should no longer have authority",
                    ]
                )
                self.assertEqual(stale_decider_code, 2)

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:decider-b"])
                stale_assessment_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        first_assessment["assessment_id"],
                        "--reason",
                        "Stale assessor evidence should no longer authorize decision",
                    ]
                )
                self.assertEqual(stale_assessment_code, 2)

                success_code, decision_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        second_assessment["assessment_id"],
                        "--reason",
                        "Reassigned reviewers now control the case",
                    ]
                )
                self.assertEqual(success_code, 0)
                self.assertEqual(
                    decision_event["payload"]["standing_decision"]["decided_by"],
                    "agent:continuum:decider-b",
                )

                standing_code, standing = self.run_cli(
                    [
                        "query",
                        "standing-state",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                    ]
                )
                self.assertEqual(standing_code, 0)
                case = standing["cases"][0]
                self.assertEqual(case["assigned_assessor_agent_ids"], ["agent:continuum:assessor-b"])
                self.assertEqual(case["assigned_decider_agent_ids"], ["agent:continuum:decider-b"])
                self.assertEqual(len(case["assignment_history"]), 1)
            finally:
                os.chdir(cwd)

    def test_continuity_case_reassignment_uses_constitution_policy_and_records_authority_basis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                for name in ("subject", "gatekeeper", "transfer-admin", "assessor-a", "assessor-b", "decider-a", "decider-b"):
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            name,
                            "--display-name",
                            f"Continuum {name.title()}",
                        ]
                    )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:subject"])
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Subject",
                        "--description",
                        "Subject under constitution-scoped reassignment",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Reassignment under constitution policy",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor-a"])
                _, first_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                continuity_policies = {
                    "case_open": {
                        "allowed_standings": ["clear"],
                        "required_roles": ["reviewer"],
                        "allow_subject_self_open": False,
                    },
                    "case_assign": {
                        "allowed_standings": ["clear"],
                        "required_roles": ["maintainer"],
                        "allow_subject_self_assign": False,
                    },
                    "case_decide": {
                        "allowed_standings": ["clear"],
                        "required_roles": ["reviewer"],
                        "allow_subject_self_decide": False,
                        "allow_opener_as_decider": False,
                        "min_assessment_count": 1,
                        "require_distinct_assessors": False,
                    },
                }
                _, constitution_event = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--continuity-policies-json",
                        json.dumps(continuity_policies, sort_keys=True),
                    ]
                )
                for reviewer in ("gatekeeper", "assessor-a", "assessor-b", "decider-a", "decider-b"):
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            "community:continuum:lab",
                            "--member-agent-id",
                            f"agent:continuum:{reviewer}",
                            "--role",
                            "reviewer",
                        ]
                    )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:transfer-admin",
                        "--role",
                        "maintainer",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )

                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "operator_handoff",
                        "--assessment-ref",
                        first_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor-a",
                        "--decider-agent-id",
                        "agent:continuum:decider-a",
                        "--linked-ref",
                        migration["event_id"],
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:assessor-b"])
                _, second_assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--actor-id",
                        "agent:continuum:subject",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:gatekeeper"])
                blocked_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "reassign",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-ref",
                        second_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor-b",
                        "--decider-agent-id",
                        "agent:continuum:decider-b",
                        "--reason",
                        "Reviewer alone should not control authority transfer",
                    ]
                )
                self.assertEqual(blocked_code, 2)

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:transfer-admin"])
                reassign_code, reassign_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "reassign",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-ref",
                        second_assessment["assessment_id"],
                        "--assessor-agent-id",
                        "agent:continuum:assessor-b",
                        "--decider-agent-id",
                        "agent:continuum:decider-b",
                        "--reason",
                        "Maintainer transfers reviewer authority under constitution policy",
                    ]
                )
                self.assertEqual(reassign_code, 0)
                assignment = reassign_event["payload"]["case_assignment"]
                self.assertEqual(
                    assignment["constitution_ref"],
                    constitution_event["payload"]["constitution"]["constitution_id"],
                )
                self.assertEqual(assignment["policy_key"], "case_assign")
                self.assertEqual(assignment["assigned_by"], "agent:continuum:transfer-admin")
            finally:
                os.chdir(cwd)

    def test_continuity_review_policies_block_subject_self_open_and_opener_self_decide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "subject",
                        "--display-name",
                        "Continuum Subject",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "reviewer",
                        "--display-name",
                        "Continuum Reviewer",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:reviewer"])
                self.run_cli(["governance", "constitution", "set", "--community-id", "community:continuum:lab"])
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:reviewer",
                        "--role",
                        "reviewer",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:subject",
                        "--role",
                        "member",
                    ]
                )

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:subject"])
                subject_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "operator_handoff",
                    ]
                )
                self.assertEqual(subject_code, 2)

                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:reviewer"])
                _, profile = self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Reviewer",
                        "--description",
                        "Reviewer for continuity authority tests",
                    ]
                )
                _, checkpoint = self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Reviewer-authored continuity evidence",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "session_restart",
                        "--from-ref",
                        "session:continuum:test-old",
                        "--to-ref",
                        "session:continuum:test-new",
                        "--reason",
                        "Test continuity review policy enforcement",
                    ]
                )
                _, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:subject",
                        "--trigger-type",
                        "declared_migration",
                        "--assessment-ref",
                        assessment["assessment_id"],
                        "--linked-ref",
                        profile["event_id"],
                        "--linked-ref",
                        checkpoint["event_id"],
                    ]
                )
                decide_code, _ = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        assessment["assessment_id"],
                        "--reason",
                        "Openers should not self-decide when separation is required",
                    ]
                )
                self.assertEqual(decide_code, 2)
            finally:
                os.chdir(cwd)

    def test_governance_state_tracks_membership_proposal_vote_and_work_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Lab Constitution",
                        "--purpose",
                        "Make governance policy explicit.",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "member",
                    ]
                )
                _, proposal = self.run_cli(
                    [
                        "governance",
                        "proposal",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-type",
                        "operational",
                        "--title",
                        "Adopt runbook skeleton",
                        "--summary",
                        "Create initial operator runbook",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "vote",
                        "cast",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-id",
                        proposal["payload"]["proposal"]["proposal_id"],
                        "--choice",
                        "for",
                    ]
                )
                _, work_item = self.run_cli(
                    [
                        "work",
                        "item",
                        "create",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Draft operator runbook",
                        "--intent",
                        "Prepare Gate 5 operator artifact",
                        "--work-type",
                        "research",
                        "--success-criterion",
                        "Runbook covers reconstruction",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "claim",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        work_item["payload"]["work_item"]["work_id"],
                        "--claim-type",
                        "take_ownership",
                    ]
                )
                _, receipt = self.run_cli(
                    [
                        "work",
                        "receipt",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        work_item["payload"]["work_item"]["work_id"],
                        "--output-ref",
                        "docs/OPERATOR_RUNBOOK_V0.md",
                        "--result-summary",
                        "Initial runbook drafted",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "evaluation",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--decision",
                        "accepted",
                        "--criteria-result",
                        "Reconstruction steps documented",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "reward",
                        "decide",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--reward-type",
                        "reputation_grant",
                        "--policy-ref",
                        "policy:work:accepted",
                    ]
                )

                code, governance_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                self.assertEqual(code, 0)
                self.assertEqual(
                    governance_state["membership_by_agent"]["agent:continuum:main"]["membership_status"],
                    "active",
                )
                self.assertEqual(governance_state["latest_constitution"]["title"], "Continuum Lab Constitution")
                self.assertEqual(len(governance_state["proposals"]), 1)
                self.assertEqual(governance_state["proposals"][0]["tallies"]["for"], 1.0)
                self.assertEqual(len(governance_state["work_items"]), 1)
                self.assertEqual(
                    governance_state["work_items"][0]["receipts"][0]["evaluation"]["decision"],
                    "accepted",
                )
                self.assertEqual(
                    governance_state["work_items"][0]["receipts"][0]["reward_decision"]["decision_status"],
                    "approved",
                )
            finally:
                os.chdir(cwd)

    def test_constitution_reward_policy_requires_treasurer_role(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                reward_policies = json.dumps(
                    {
                        "treasury_payment": {
                            "approver_roles": ["treasurer"],
                            "approver_standings": ["clear"],
                            "beneficiary_standings": ["clear"],
                        }
                    },
                    sort_keys=True,
                )
                self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Treasury Role Constitution",
                        "--reward-policies-json",
                        reward_policies,
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "member",
                    ]
                )
                _, work_item = self.run_cli(
                    [
                        "work",
                        "item",
                        "create",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Maintain relay",
                        "--intent",
                        "Keep local infra healthy",
                        "--work-type",
                        "maintenance",
                        "--success-criterion",
                        "Maintenance artifact recorded",
                    ]
                )
                _, receipt = self.run_cli(
                    [
                        "work",
                        "receipt",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        work_item["payload"]["work_item"]["work_id"],
                        "--output-ref",
                        "docs/OPERATOR_RUNBOOK_V0.md",
                        "--result-summary",
                        "Maintenance completed",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "evaluation",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--decision",
                        "accepted",
                        "--criteria-result",
                        "Maintenance verified",
                    ]
                )

                self.assertEqual(
                    self.run_cli(
                        [
                            "governance",
                            "reward",
                            "decide",
                            "--community-id",
                            "community:continuum:lab",
                            "--receipt-id",
                            receipt["payload"]["work_receipt"]["receipt_id"],
                            "--reward-type",
                            "treasury_payment",
                            "--policy-ref",
                            "policy:treasury:maintenance",
                        ]
                    )[0],
                    2,
                )

                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "member",
                        "--role",
                        "treasurer",
                    ]
                )
                code, reward_event = self.run_cli(
                    [
                        "governance",
                        "reward",
                        "decide",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--reward-type",
                        "treasury_payment",
                        "--policy-ref",
                        "policy:treasury:maintenance",
                    ]
                )
                self.assertEqual(code, 0)
                self.assertEqual(reward_event["payload"]["reward_decision"]["decision_status"], "approved")
            finally:
                os.chdir(cwd)

    def test_restricted_standing_blocks_treasury_vote_and_withholds_treasury_reward(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "approver",
                        "--display-name",
                        "Continuum Approver",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:approver",
                        "--role",
                        "treasurer",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                        "--agent-id",
                        "agent:continuum:main",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "reviewer",
                        "--display-name",
                        "Continuum Reviewer",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "decider",
                        "--display-name",
                        "Continuum Decider",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:reviewer",
                        "--role",
                        "reviewer",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:decider",
                        "--role",
                        "reviewer",
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:main"])
                _, treasury_proposal = self.run_cli(
                    [
                        "governance",
                        "proposal",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-type",
                        "treasury",
                        "--title",
                        "Fund storage relay",
                        "--summary",
                        "Allocate maintenance budget",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Checkpoint one",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "operator_change",
                        "--from-ref",
                        "operator:founder",
                        "--to-ref",
                        "operator:successor",
                        "--reason",
                        "Declared handoff",
                        "--community-id",
                        "community:continuum:lab",
                    ]
                )
                _, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:reviewer"])
                _, case_event = self.run_cli(
                    [
                        "continuity",
                        "case",
                        "open",
                        "--community-id",
                        "community:continuum:lab",
                        "--subject-agent-id",
                        "agent:continuum:main",
                        "--trigger-type",
                        "operator_handoff",
                        "--assessment-ref",
                        assessment["assessment_id"],
                        "--linked-ref",
                        migration["event_id"],
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:decider"])
                self.run_cli(
                    [
                        "continuity",
                        "case",
                        "decide",
                        "--case-event-id",
                        case_event["event_id"],
                        "--assessment-id",
                        assessment["assessment_id"],
                        "--reason",
                        "Restricted successor standing",
                    ]
                )
                self.run_cli(["agent", "use", "--agent-id", "agent:continuum:main"])

                vote_code, _ = self.run_cli(
                    [
                        "governance",
                        "vote",
                        "cast",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-id",
                        treasury_proposal["payload"]["proposal"]["proposal_id"],
                        "--choice",
                        "for",
                    ]
                )
                self.assertEqual(vote_code, 2)

                _, work_item = self.run_cli(
                    [
                        "work",
                        "item",
                        "create",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Repair relay storage",
                        "--intent",
                        "Restore local relay durability",
                        "--work-type",
                        "maintenance",
                        "--success-criterion",
                        "Relay state rebuilt",
                    ]
                )
                _, receipt = self.run_cli(
                    [
                        "work",
                        "receipt",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        work_item["payload"]["work_item"]["work_id"],
                        "--output-ref",
                        "src/runtime/store.py",
                        "--result-summary",
                        "Storage patch applied",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "evaluation",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--decision",
                        "accepted",
                        "--criteria-result",
                        "Patch landed",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "approver",
                        "--display-name",
                        "Continuum Approver",
                        "--agent-id",
                        "agent:continuum:approver",
                    ]
                )
                reward_code, reward_event = self.run_cli(
                    [
                        "governance",
                        "reward",
                        "decide",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--reward-type",
                        "treasury_payment",
                        "--policy-ref",
                        "policy:treasury:maintenance",
                        "--amount",
                        "100",
                    ]
                )
                self.assertEqual(reward_code, 0)
                self.assertEqual(
                    reward_event["payload"]["reward_decision"]["decision_status"],
                    "withheld_pending_review",
                )
                self.assertEqual(
                    reward_event["payload"]["reward_decision"]["withholding_reason"],
                    "beneficiary_standing_suspended",
                )
            finally:
                os.chdir(cwd)

    def test_constitution_supersession_materializes_lineage_and_latest_constitution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                _, first_constitution = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v1",
                        "--constitution-version",
                        "v1",
                        "--amended-at",
                        "2026-03-22T00:00:00Z",
                    ]
                )
                first_id = first_constitution["payload"]["constitution"]["constitution_id"]

                self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2",
                        "--constitution-version",
                        "v2",
                        "--supersedes",
                        first_id,
                        "--amended-at",
                        "2026-03-22T01:00:00Z",
                    ]
                )

                _, governance_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                self.assertEqual(governance_state["latest_constitution"]["constitution_version"], "v2")
                self.assertEqual(governance_state["constitution_replay_warnings"], [])
                lineage = governance_state["constitution_lineage"]
                self.assertEqual(len(lineage), 2)
                first_entry = next(entry for entry in lineage if entry["constitution_id"] == first_id)
                latest_id = governance_state["latest_constitution"]["constitution_id"]
                second_entry = next(entry for entry in lineage if entry["constitution_id"] == latest_id)
                self.assertEqual(first_entry["lineage_state"], "superseded")
                self.assertEqual(second_entry["lineage_state"], "active")
                self.assertEqual(second_entry["supersedes"], first_id)
            finally:
                os.chdir(cwd)

    def test_constitution_conflict_can_be_resolved_into_canonical_branch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "maintainer",
                        "--role",
                        "member",
                    ]
                )
                _, root_constitution = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v1",
                        "--constitution-version",
                        "v1",
                        "--amended-at",
                        "2026-03-22T00:00:00Z",
                    ]
                )
                root_id = root_constitution["payload"]["constitution"]["constitution_id"]
                _, branch_a = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2-a",
                        "--constitution-version",
                        "v2-a",
                        "--supersedes",
                        root_id,
                        "--amended-at",
                        "2026-03-22T01:00:00Z",
                    ]
                )
                _, branch_b = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2-b",
                        "--constitution-version",
                        "v2-b",
                        "--supersedes",
                        root_id,
                        "--amended-at",
                        "2026-03-22T01:05:00Z",
                    ]
                )
                branch_a_id = branch_a["payload"]["constitution"]["constitution_id"]
                branch_b_id = branch_b["payload"]["constitution"]["constitution_id"]

                _, governance_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                self.assertEqual(governance_state["latest_constitution"]["constitution_id"], branch_b_id)
                self.assertIn(f"constitution_conflict:{root_id}", governance_state["constitution_replay_warnings"])
                conflicted_ids = {
                    entry["constitution_id"]
                    for entry in governance_state["constitution_lineage"]
                    if entry["lineage_state"] == "conflicted"
                }
                self.assertEqual(conflicted_ids, {branch_a_id, branch_b_id})

                _, resolution_event = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "resolve",
                        "--community-id",
                        "community:continuum:lab",
                        "--parent-constitution-id",
                        root_id,
                        "--recognized-constitution-id",
                        branch_b_id,
                        "--rejected-constitution-id",
                        branch_a_id,
                        "--reason",
                        "Choose the canonical amendment branch for replay.",
                    ]
                )

                _, governance_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                self.assertEqual(governance_state["latest_constitution"]["constitution_id"], branch_b_id)
                self.assertNotIn(f"constitution_conflict:{root_id}", governance_state["constitution_replay_warnings"])
                self.assertIn(
                    f"constitution_resolution_missing_proposal:{resolution_event['payload']['constitution_resolution']['resolution_id']}",
                    governance_state["constitution_replay_warnings"],
                )
                self.assertIn(
                    f"constitution_resolution_missing_execution:{resolution_event['payload']['constitution_resolution']['resolution_id']}",
                    governance_state["constitution_replay_warnings"],
                )
                self.assertEqual(len(governance_state["constitution_resolutions"]), 1)
                lineage = governance_state["constitution_lineage"]
                branch_a_entry = next(entry for entry in lineage if entry["constitution_id"] == branch_a_id)
                branch_b_entry = next(entry for entry in lineage if entry["constitution_id"] == branch_b_id)
                self.assertEqual(branch_a_entry["lineage_state"], "rejected")
                self.assertEqual(branch_b_entry["lineage_state"], "active")
                self.assertEqual(
                    branch_a_entry["resolution_ref"],
                    resolution_event["payload"]["constitution_resolution"]["resolution_id"],
                )
                self.assertEqual(
                    branch_b_entry["resolution_ref"],
                    resolution_event["payload"]["constitution_resolution"]["resolution_id"],
                )
            finally:
                os.chdir(cwd)

    def test_constitution_resolution_can_reference_proposal_and_execution_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "maintainer",
                        "--role",
                        "member",
                    ]
                )
                _, root_constitution = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v1",
                        "--constitution-version",
                        "v1",
                        "--amended-at",
                        "2026-03-22T00:00:00Z",
                    ]
                )
                root_id = root_constitution["payload"]["constitution"]["constitution_id"]
                _, branch_a = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2-a",
                        "--constitution-version",
                        "v2-a",
                        "--supersedes",
                        root_id,
                        "--amended-at",
                        "2026-03-22T01:00:00Z",
                    ]
                )
                _, branch_b = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2-b",
                        "--constitution-version",
                        "v2-b",
                        "--supersedes",
                        root_id,
                        "--amended-at",
                        "2026-03-22T01:05:00Z",
                    ]
                )
                branch_a_id = branch_a["payload"]["constitution"]["constitution_id"]
                branch_b_id = branch_b["payload"]["constitution"]["constitution_id"]
                _, proposal_event = self.run_cli(
                    [
                        "governance",
                        "proposal",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-type",
                        "constitutional",
                        "--title",
                        "Recognize canonical constitutional branch",
                        "--summary",
                        "Select the branch that should count as canonical for replay.",
                        "--affected-ref",
                        branch_a_id,
                        "--affected-ref",
                        branch_b_id,
                    ]
                )
                proposal_id = proposal_event["payload"]["proposal"]["proposal_id"]
                _, resolution_event = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "resolve",
                        "--community-id",
                        "community:continuum:lab",
                        "--parent-constitution-id",
                        root_id,
                        "--recognized-constitution-id",
                        branch_b_id,
                        "--rejected-constitution-id",
                        branch_a_id,
                        "--proposal-ref",
                        proposal_id,
                        "--reason",
                        "Select the canonical amendment branch for replay.",
                    ]
                )
                resolution_id = resolution_event["payload"]["constitution_resolution"]["resolution_id"]
                self.run_cli(
                    [
                        "governance",
                        "execute",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--execution-type",
                        "constitution_execution",
                        "--governed-ref",
                        resolution_id,
                        "--governed-ref",
                        proposal_id,
                        "--output-ref",
                        "doc://constitution-resolution/branch-b",
                        "--result-summary",
                        "Recorded the canonical constitutional branch and published replay references.",
                    ]
                )

                _, governance_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                resolution_view = governance_state["constitution_resolutions"][0]
                self.assertEqual(resolution_view["proposal"]["proposal_id"], proposal_id)
                self.assertEqual(len(resolution_view["execution_receipts"]), 1)
                self.assertEqual(
                    resolution_view["execution_receipts"][0]["execution_type"],
                    "constitution_execution",
                )
                self.assertNotIn(
                    f"constitution_resolution_missing_proposal:{resolution_id}",
                    governance_state["constitution_replay_warnings"],
                )
                self.assertNotIn(
                    f"constitution_resolution_missing_execution:{resolution_id}",
                    governance_state["constitution_replay_warnings"],
                )
            finally:
                os.chdir(cwd)

    def test_constitution_resolution_policy_can_require_proposal_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                continuity_policies = json.dumps(
                    {
                        "case_open": {
                            "allowed_standings": ["clear"],
                            "required_roles": ["maintainer", "reviewer"],
                            "allow_subject_self_open": False,
                        },
                        "case_assign": {
                            "allowed_standings": ["clear"],
                            "required_roles": ["maintainer"],
                            "allow_subject_self_assign": False,
                        },
                        "case_decide": {
                            "allowed_standings": ["clear"],
                            "required_roles": ["maintainer", "reviewer"],
                            "allow_subject_self_decide": False,
                            "allow_opener_as_decider": False,
                            "min_assessment_count": 1,
                            "require_distinct_assessors": False,
                        },
                        "constitution_resolution": {
                            "allowed_standings": ["clear"],
                            "required_roles": ["maintainer"],
                            "require_proposal_ref": True,
                            "require_execution_receipt": False,
                        },
                    },
                    sort_keys=True,
                )
                self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--continuity-policies-json",
                        continuity_policies,
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "maintainer",
                        "--role",
                        "member",
                    ]
                )
                _, root_constitution = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v1",
                        "--constitution-version",
                        "v1",
                        "--amended-at",
                        "2026-03-22T00:00:00Z",
                    ]
                )
                root_id = root_constitution["payload"]["constitution"]["constitution_id"]
                _, branch_a = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2-a",
                        "--constitution-version",
                        "v2-a",
                        "--supersedes",
                        root_id,
                        "--amended-at",
                        "2026-03-22T01:00:00Z",
                    ]
                )
                _, branch_b = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Constitution v2-b",
                        "--constitution-version",
                        "v2-b",
                        "--supersedes",
                        root_id,
                        "--amended-at",
                        "2026-03-22T01:05:00Z",
                    ]
                )
                branch_a_id = branch_a["payload"]["constitution"]["constitution_id"]
                branch_b_id = branch_b["payload"]["constitution"]["constitution_id"]

                resolution_code, _ = self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "resolve",
                        "--community-id",
                        "community:continuum:lab",
                        "--parent-constitution-id",
                        root_id,
                        "--recognized-constitution-id",
                        branch_b_id,
                        "--rejected-constitution-id",
                        branch_a_id,
                        "--reason",
                        "Attempt resolution without proposal basis.",
                    ]
                )
                self.assertEqual(resolution_code, 2)
            finally:
                os.chdir(cwd)

    def test_governance_execution_receipt_attaches_to_proposal_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(["governance", "constitution", "set", "--community-id", "community:continuum:lab"])
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                        "--role",
                        "maintainer",
                        "--role",
                        "member",
                    ]
                )
                _, proposal_event = self.run_cli(
                    [
                        "governance",
                        "proposal",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--proposal-type",
                        "operational",
                        "--title",
                        "Execute lab step",
                        "--summary",
                        "Create an execution receipt for proposal replay.",
                    ]
                )
                proposal_id = proposal_event["payload"]["proposal"]["proposal_id"]
                self.run_cli(
                    [
                        "governance",
                        "execute",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--execution-type",
                        "proposal_execution",
                        "--governed-ref",
                        proposal_id,
                        "--output-ref",
                        "docs/OPERATOR_RUNBOOK_V0.md",
                        "--result-summary",
                        "Operational proposal executed in repository-local demo.",
                    ]
                )
                _, governance_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                proposal_state = governance_state["proposals"][0]
                self.assertEqual(len(proposal_state["execution_receipts"]), 1)
                self.assertEqual(
                    proposal_state["execution_receipts"][0]["execution_type"],
                    "proposal_execution",
                )
            finally:
                os.chdir(cwd)

    def test_anchor_export_is_deterministic_for_governance_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "membership",
                        "grant",
                        "--community-id",
                        "community:continuum:lab",
                        "--member-agent-id",
                        "agent:continuum:main",
                    ]
                )
                self.run_cli(
                    [
                        "governance",
                        "constitution",
                        "set",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Continuum Lab Constitution",
                    ]
                )
                first_code, first_anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "governance_state_root",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                        "--anchored-at",
                        "2026-03-21T12:00:00Z",
                    ]
                )
                second_code, second_anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "governance_state_root",
                        "--community-id",
                        "community:continuum:lab",
                        "--anchored-at",
                        "2026-03-21T12:00:00Z",
                    ]
                )
                self.assertEqual(first_code, 0)
                self.assertEqual(second_code, 0)
                self.assertEqual(first_anchor["anchor_id"], second_anchor["anchor_id"])
                self.assertEqual(first_anchor["root_hash"], second_anchor["root_hash"])

                list_code, anchors = self.run_cli(
                    [
                        "anchor",
                        "list",
                        "--subject-ref",
                        "community:continuum:lab",
                        "--anchor-type",
                        "governance_state_root",
                    ]
                )
                self.assertEqual(list_code, 0)
                self.assertEqual(len(anchors["anchors"]), 1)
            finally:
                os.chdir(cwd)

    def test_anchor_export_supports_assessment_and_fresh_session_reconstruction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in (
                    "FOUNDING_THESIS.md",
                    "OPERATING_MODEL.md",
                    "TASK_BOARD.md",
                    "REVISION_LOG.md",
                ):
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )
                self.run_cli(
                    [
                        "agent",
                        "profile",
                        "set",
                        "--display-name",
                        "Continuum Main",
                        "--description",
                        "Bootstrap agent",
                    ]
                )
                self.run_cli(
                    [
                        "memory",
                        "checkpoint",
                        "create",
                        "--scope",
                        "session_handoff",
                        "--summary",
                        "Checkpoint one",
                    ]
                )
                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "session_restart",
                        "--from-ref",
                        "session:continuum:run-old",
                        "--to-ref",
                        "session:continuum:run-new",
                        "--reason",
                        "Automation restart",
                    ]
                )
                _, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )

                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                        "--agent-id",
                        "agent:continuum:main",
                    ]
                )
                code, anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "continuity_assessment_root",
                        "--assessment-id",
                        assessment["assessment_id"],
                        "--anchored-at",
                        "2026-03-21T13:00:00Z",
                    ]
                )
                self.assertEqual(code, 0)
                self.assertEqual(anchor["subject_ref"], assessment["assessment_id"])
                self.assertTrue(anchor["root_hash"].startswith("state:"))

                inspect_code, inspected = self.run_cli(["anchor", "inspect", "--anchor-id", anchor["anchor_id"]])
                self.assertEqual(inspect_code, 0)
                self.assertEqual(inspected["anchor_id"], anchor["anchor_id"])
            finally:
                os.chdir(cwd)

    def test_governance_state_isolates_work_claims_and_evaluations_by_community(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                self.run_cli(
                    [
                        "agent",
                        "init",
                        "--scope",
                        "continuum",
                        "--name",
                        "main",
                        "--display-name",
                        "Continuum Main",
                    ]
                )

                for community_id, title in (
                    ("community:continuum:lab", "Continuum Lab Constitution"),
                    ("community:continuum:forge", "Continuum Forge Constitution"),
                ):
                    self.run_cli(
                        [
                            "governance",
                            "constitution",
                            "set",
                            "--community-id",
                            community_id,
                            "--title",
                            title,
                        ]
                    )
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            community_id,
                            "--member-agent-id",
                            "agent:continuum:main",
                            "--role",
                            "member",
                        ]
                    )

                _, lab_work = self.run_cli(
                    [
                        "work",
                        "item",
                        "create",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Lab runbook maintenance",
                        "--intent",
                        "Keep lab docs current",
                        "--work-type",
                        "maintenance",
                        "--success-criterion",
                        "Lab docs updated",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "claim",
                        "submit",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        lab_work["payload"]["work_item"]["work_id"],
                        "--claim-type",
                        "take_ownership",
                    ]
                )
                _, lab_receipt = self.run_cli(
                    [
                        "work",
                        "receipt",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        lab_work["payload"]["work_item"]["work_id"],
                        "--output-ref",
                        "docs/OPERATOR_RUNBOOK_V0.md",
                        "--result-summary",
                        "Lab runbook updated",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "evaluation",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        lab_receipt["payload"]["work_receipt"]["receipt_id"],
                        "--decision",
                        "accepted",
                        "--criteria-result",
                        "Lab update verified",
                    ]
                )

                _, forge_work = self.run_cli(
                    [
                        "work",
                        "item",
                        "create",
                        "--community-id",
                        "community:continuum:forge",
                        "--title",
                        "Forge policy draft",
                        "--intent",
                        "Draft forge policy",
                        "--work-type",
                        "research",
                        "--success-criterion",
                        "Forge policy captured",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "claim",
                        "submit",
                        "--community-id",
                        "community:continuum:forge",
                        "--work-id",
                        forge_work["payload"]["work_item"]["work_id"],
                        "--claim-type",
                        "take_ownership",
                    ]
                )
                _, forge_receipt = self.run_cli(
                    [
                        "work",
                        "receipt",
                        "record",
                        "--community-id",
                        "community:continuum:forge",
                        "--work-id",
                        forge_work["payload"]["work_item"]["work_id"],
                        "--output-ref",
                        "docs/OPERATING_MODEL.md",
                        "--result-summary",
                        "Forge policy drafted",
                    ]
                )
                self.run_cli(
                    [
                        "work",
                        "evaluation",
                        "record",
                        "--community-id",
                        "community:continuum:forge",
                        "--receipt-id",
                        forge_receipt["payload"]["work_receipt"]["receipt_id"],
                        "--decision",
                        "accepted_with_issues",
                        "--criteria-result",
                        "Forge draft needs revision",
                    ]
                )

                _, lab_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                _, forge_state = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:forge", "--refresh"]
                )

                self.assertEqual(len(lab_state["work_claims"]), 1)
                self.assertEqual(len(lab_state["work_evaluations"]), 1)
                self.assertEqual(lab_state["work_claims"][0]["work_id"], lab_work["payload"]["work_item"]["work_id"])
                self.assertEqual(
                    lab_state["work_evaluations"][0]["receipt_id"],
                    lab_receipt["payload"]["work_receipt"]["receipt_id"],
                )

                self.assertEqual(len(forge_state["work_claims"]), 1)
                self.assertEqual(len(forge_state["work_evaluations"]), 1)
                self.assertEqual(
                    forge_state["work_claims"][0]["work_id"],
                    forge_work["payload"]["work_item"]["work_id"],
                )
                self.assertEqual(
                    forge_state["work_evaluations"][0]["receipt_id"],
                    forge_receipt["payload"]["work_receipt"]["receipt_id"],
                )
            finally:
                os.chdir(cwd)

    def test_demo_fixture_replays_v0_narrative_with_anchorable_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path.cwd()
            try:
                os.chdir(tmp)
                scenario_path = Path(__file__).resolve().parent / "fixtures" / "continuum_demo_v0.json"
                scenario = json.loads(scenario_path.read_text(encoding="utf-8"))

                docs_dir = Path(tmp) / "docs"
                docs_dir.mkdir(parents=True, exist_ok=True)
                for artifact in scenario["required_repository_artifacts"]:
                    (docs_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")

                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "init",
                            "--scope",
                            "continuum",
                            "--name",
                            "main",
                            "--display-name",
                            "Continuum Main",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "agent",
                            "profile",
                            "set",
                            "--display-name",
                            "Continuum Main",
                            "--description",
                            "Repository-local continuity operator",
                            "--artifact-ref",
                            "docs/FOUNDING_THESIS.md",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "memory",
                            "checkpoint",
                            "create",
                            "--scope",
                            "session_handoff",
                            "--summary",
                            "Fresh session reconstruction complete",
                            "--artifact-ref",
                            "docs/TASK_BOARD.md",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "governance",
                            "constitution",
                            "set",
                            "--community-id",
                            "community:continuum:lab",
                            "--title",
                            "Continuum Lab Constitution",
                            "--purpose",
                            "Keep governance legible and continuity-aware.",
                            "--artifact-ref",
                            "docs/OPERATING_MODEL.md",
                        ]
                    )[0],
                    0,
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "governance",
                            "membership",
                            "grant",
                            "--community-id",
                            "community:continuum:lab",
                            "--member-agent-id",
                            "agent:continuum:main",
                            "--role",
                            "member",
                        ]
                    )[0],
                    0,
                )
                _, work_item = self.run_cli(
                    [
                        "work",
                        "item",
                        "create",
                        "--community-id",
                        "community:continuum:lab",
                        "--title",
                        "Preserve continuity demo path",
                        "--intent",
                        "Keep the repository-local Continuum demo replayable.",
                        "--work-type",
                        "maintenance",
                        "--success-criterion",
                        "Demo artifacts and anchors remain reproducible.",
                    ]
                )
                _, receipt = self.run_cli(
                    [
                        "work",
                        "receipt",
                        "record",
                        "--community-id",
                        "community:continuum:lab",
                        "--work-id",
                        work_item["payload"]["work_item"]["work_id"],
                        "--output-ref",
                        "docs/OPERATOR_RUNBOOK_V0.md",
                        "--result-summary",
                        "Demo path recorded and verified",
                    ]
                )
                self.assertEqual(
                    self.run_cli(
                        [
                            "work",
                            "evaluation",
                            "record",
                            "--community-id",
                            "community:continuum:lab",
                            "--receipt-id",
                            receipt["payload"]["work_receipt"]["receipt_id"],
                            "--decision",
                            "accepted",
                            "--criteria-result",
                            "Runbook and fixtures support replay",
                        ]
                    )[0],
                    0,
                )
                reward_code, reward = self.run_cli(
                    [
                        "governance",
                        "reward",
                        "decide",
                        "--community-id",
                        "community:continuum:lab",
                        "--receipt-id",
                        receipt["payload"]["work_receipt"]["receipt_id"],
                        "--reward-type",
                        "treasury_payment",
                        "--policy-ref",
                        "policy:treasury:demo",
                        "--amount",
                        "42",
                    ]
                )
                self.assertEqual(reward_code, 0)
                self.assertEqual(reward["payload"]["reward_decision"]["decision_status"], "approved")

                _, migration = self.run_cli(
                    [
                        "migration",
                        "declare",
                        "--migration-type",
                        "session_restart",
                        "--from-ref",
                        "session:continuum:demo-old",
                        "--to-ref",
                        "session:continuum:demo-new",
                        "--reason",
                        "Repository reconstruction after automation restart",
                        "--artifact-ref",
                        "docs/REVISION_LOG.md",
                    ]
                )
                assessment_code, assessment = self.run_cli(
                    [
                        "continuity",
                        "assess",
                        "--event-id",
                        migration["event_id"],
                        "--refresh",
                    ]
                )
                self.assertEqual(assessment_code, 0)
                self.assertEqual(assessment["continuity_class"], scenario["expected_assessment"]["continuity_class"])
                self.assertEqual(
                    assessment["recognition_readiness"],
                    scenario["expected_assessment"]["recognition_readiness"],
                )

                standing_code, standing = self.run_cli(
                    [
                        "query",
                        "standing-state",
                        "--subject-agent-id",
                        "agent:continuum:main",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                    ]
                )
                self.assertEqual(standing_code, 0)
                self.assertEqual(standing["current_standing"], scenario["expected_standing"])

                governance_code, governance = self.run_cli(
                    ["query", "governance-state", "--community-id", "community:continuum:lab", "--refresh"]
                )
                self.assertEqual(governance_code, 0)
                self.assertEqual(len(governance["work_items"]), 1)
                self.assertEqual(
                    governance["work_items"][0]["receipts"][0]["reward_decision"]["decision_status"],
                    "approved",
                )

                assessment_anchor_code, assessment_anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "continuity_assessment_root",
                        "--assessment-id",
                        assessment["assessment_id"],
                        "--anchored-at",
                        "2026-03-21T14:00:00Z",
                    ]
                )
                self.assertEqual(assessment_anchor_code, 0)
                self.assertEqual(assessment_anchor["subject_ref"], assessment["assessment_id"])
                self.assertTrue(assessment_anchor["root_hash"].startswith("state:"))

                governance_anchor_code, governance_anchor = self.run_cli(
                    [
                        "anchor",
                        "export",
                        "--anchor-type",
                        "governance_state_root",
                        "--community-id",
                        "community:continuum:lab",
                        "--refresh",
                        "--anchored-at",
                        "2026-03-21T14:05:00Z",
                    ]
                )
                self.assertEqual(governance_anchor_code, 0)
                self.assertEqual(governance_anchor["subject_ref"], "community:continuum:lab")
                self.assertTrue(governance_anchor["root_hash"].startswith("state:"))

                list_code, anchors = self.run_cli(["anchor", "list"])
                self.assertEqual(list_code, 0)
                self.assertEqual(len(anchors["anchors"]), len(scenario["expected_anchor_types"]))
                self.assertEqual(
                    sorted(anchor["anchor_type"] for anchor in anchors["anchors"]),
                    sorted(scenario["expected_anchor_types"]),
                )
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
