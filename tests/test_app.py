"""Tests for the application orchestrator and menu wiring."""
from __future__ import annotations

from pathlib import Path

import pytest

from quadrainspect.app import QuadraInspect
from quadrainspect.exceptions import CommandError
from quadrainspect.session import Workspace


def make_app(tmp_path: Path) -> QuadraInspect:
    return QuadraInspect(Workspace.from_path(tmp_path), dry_run=True)


def test_menu_entries_have_frame_or_arg_name(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    for entry in app.entries:
        assert entry.frame_name or entry.arg_name
        assert entry.description
        assert callable(entry.action)


def test_frame_and_argument_modes_share_actions(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    # Every argument-mode command must correspond to exactly one entry.
    arg_names = [e.arg_name for e in app.entries if e.arg_name]
    assert len(arg_names) == len(set(arg_names))
    # SET target is interactive-only (no argument-mode equivalent).
    set_target = next(e for e in app.entries if e.frame_name == "SET target")
    assert set_target.arg_name is None


def test_argument_mode_unknown_command_raises(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    with pytest.raises(CommandError):
        app.run_argument("does-not-exist")


@pytest.mark.parametrize("command", ["banner", "tools_name", "mobfs", "rms"])
def test_argument_mode_safe_commands_run(tmp_path: Path, command: str) -> None:
    # dry_run means external tools are logged, not executed.
    app = make_app(tmp_path)
    app.run_argument(command)
    assert app.session.workspace.tools_dir.is_dir()


def test_argument_help_lists_only_arg_commands(tmp_path: Path) -> None:
    app = make_app(tmp_path)
    table = app.argument_help()
    listed = list(table.columns[0].cells)
    assert "tools_name" in listed
    assert "SET target" not in listed
