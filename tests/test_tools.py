"""Tests for the tool classes and the add-ins wiring."""
from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from quadrainspect.platform import OperatingSystem, Platform
from quadrainspect.runner import CommandRunner
from quadrainspect.session import Session, Workspace
from quadrainspect.tools import AddinsManager, BackdoorTool
from quadrainspect.tools.base import ToolContext


def make_context(tmp_path: Path) -> ToolContext:
    return ToolContext(
        session=Session(Workspace.from_path(tmp_path)),
        runner=CommandRunner(dry_run=True),
        platform=Platform(OperatingSystem.LINUX),
    )


def test_addon_install_callables_take_no_arguments(tmp_path: Path) -> None:
    # Regression: _install() must invoke addon.install() with no arguments.
    manager = AddinsManager(make_context(tmp_path))
    for addon in manager._addons.values():
        signature = inspect.signature(addon.install)
        assert len(signature.parameters) == 0


def test_addon_install_dispatch_invokes_selected_addon(tmp_path: Path, monkeypatch) -> None:
    manager = AddinsManager(make_context(tmp_path))
    called: list[str] = []
    # Replace the real (network-touching) installers with no-arg recorders.
    manager._addons["1"] = manager._addons["1"].__class__(
        key="1", name="APKEditor", os_support="all", depends="Java",
        install=lambda: called.append("apkeditor"),
    )
    monkeypatch.setattr("quadrainspect.tools.addins.Prompt.ask", lambda *a, **k: "1")
    manager._install()
    assert called == ["apkeditor"]


def test_backdoor_tool_root_matches_install_layout(tmp_path: Path) -> None:
    # The runner path and the add-on install path must agree on this directory.
    tool = BackdoorTool(make_context(tmp_path))
    expected = tmp_path / "tools" / "backdoor-apk-master" / "backdoor-apk"
    assert tool._tool_root == expected


def test_oneshot_tool_requires_execute() -> None:
    # Tool being an ABC means a OneShotTool subclass without execute() cannot
    # be instantiated.
    from quadrainspect.tools.base import OneShotTool

    class Incomplete(OneShotTool):
        name = "incomplete"

    with pytest.raises(TypeError):
        Incomplete(None)  # type: ignore[arg-type]
