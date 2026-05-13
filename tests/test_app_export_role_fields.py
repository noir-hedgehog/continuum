from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.app.export import export_agents_app_data
from src.runtime.store import RepositoryStore


class TestAppExportRoleFields(unittest.TestCase):
    def test_roles_are_marked_and_counted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            store = RepositoryStore(root)
            store.save_agent(
                {
                    "agent_id": "agent:continuum:alice",
                    "display_name": "Alice",
                    "description": "",
                    "operator_disclosure": "",
                    "signing_key": "key:continuum:alice:primary",
                    "secret_hex": "00",
                }
            )
            store.save_agent(
                {
                    "agent_id": "role:continuum:main-integrator",
                    "display_name": "Continuum Main Integrator",
                    "description": "",
                    "operator_disclosure": "",
                    "signing_key": "key:continuum:main-integrator:role-primary",
                    "secret_hex": "11",
                },
                make_current=False,
            )

            output = root / "export.json"
            export_agents_app_data(
                store,
                actor_ids=[],
                community_id="community:continuum:lab",
                output_path=output,
                refresh=True,
            )

            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["agent_count"], 2)
            self.assertEqual(payload["role_count"], 1)
            self.assertEqual(payload["non_role_agent_count"], 1)

            kinds = {entry["agent_id"]: entry["subject_kind"] for entry in payload["agents"]}
            self.assertEqual(kinds["agent:continuum:alice"], "agent")
            self.assertEqual(kinds["role:continuum:main-integrator"], "role")

