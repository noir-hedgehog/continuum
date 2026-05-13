from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.cli.main import cmd_role_list
from src.runtime.store import RepositoryStore


class TestCliRoleList(unittest.TestCase):
    def test_lists_only_roles(self) -> None:
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

            original_cwd = Path.cwd()
            try:
                os.chdir(root)
                buf = io.StringIO()
                with redirect_stdout(buf):
                    cmd_role_list(type("Args", (), {"scope": None})())
                payload = json.loads(buf.getvalue())
            finally:
                os.chdir(original_cwd)

            self.assertEqual([item["agent_id"] for item in payload["roles"]], ["role:continuum:main-integrator"])

    def test_filters_by_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            store = RepositoryStore(root)
            store.save_agent(
                {
                    "agent_id": "role:continuum:builder",
                    "display_name": "Continuum Builder",
                    "description": "",
                    "operator_disclosure": "",
                    "signing_key": "key:continuum:builder:role-primary",
                    "secret_hex": "22",
                }
            )
            store.save_agent(
                {
                    "agent_id": "role:other:thing",
                    "display_name": "Other Thing",
                    "description": "",
                    "operator_disclosure": "",
                    "signing_key": "key:other:thing:role-primary",
                    "secret_hex": "33",
                },
                make_current=False,
            )

            original_cwd = Path.cwd()
            try:
                os.chdir(root)
                buf = io.StringIO()
                with redirect_stdout(buf):
                    cmd_role_list(type("Args", (), {"scope": "continuum"})())
                payload = json.loads(buf.getvalue())
            finally:
                os.chdir(original_cwd)

            self.assertEqual([item["agent_id"] for item in payload["roles"]], ["role:continuum:builder"])

