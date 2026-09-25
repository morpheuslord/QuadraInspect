"""Unit tests for the QuadraInspect core."""
from __future__ import annotations

from pathlib import Path

import pytest

from quadrainspect.exceptions import (
    CommandError,
    DependencyError,
    TargetNotSetError,
    ToolExecutionError,
)
from quadrainspect.platform import OperatingSystem, Platform
from quadrainspect.registry import CommandRegistry
from quadrainspect.runner import CommandRunner
from quadrainspect.session import Session, Workspace


# -- Workspace -------------------------------------------------------------
def test_workspace_paths_are_relative_to_root(tmp_path: Path) -> None:
    workspace = Workspace.from_path(tmp_path)
    assert workspace.tools_dir == tmp_path / "tools"
    assert workspace.results_dir == tmp_path / "results"
    assert workspace.tool_dir("apkleaks") == tmp_path / "tools" / "apkleaks"


def test_ensure_directories_creates_all(tmp_path: Path) -> None:
    workspace = Workspace.from_path(tmp_path)
    workspace.ensure_directories()
    for directory in workspace.managed_directories:
        assert directory.is_dir()
    # Idempotent.
    workspace.ensure_directories()


# -- Session ---------------------------------------------------------------
def test_session_target_path_requires_target(tmp_path: Path) -> None:
    session = Session(Workspace.from_path(tmp_path))
    assert not session.has_target
    with pytest.raises(TargetNotSetError):
        _ = session.target_path


def test_session_target_roundtrip(tmp_path: Path) -> None:
    session = Session(Workspace.from_path(tmp_path))
    session.target = "  app.apk  "
    assert session.target == "app.apk"
    assert session.target_path == tmp_path / "target" / "app.apk"
    session.target = "   "
    assert session.target is None


# -- Registry --------------------------------------------------------------
def test_registry_dispatch_invokes_handler() -> None:
    registry = CommandRegistry()
    calls: list[str] = []
    registry.register("go", "desc", lambda: calls.append("go"))
    registry.dispatch("go")
    assert calls == ["go"]


def test_registry_unknown_command_raises() -> None:
    registry = CommandRegistry()
    with pytest.raises(CommandError):
        registry.dispatch("nope")


def test_registry_rejects_duplicates() -> None:
    registry = CommandRegistry()
    registry.register("go", "desc", lambda: None)
    with pytest.raises(CommandError):
        registry.register("go", "desc", lambda: None)


def test_registry_aliases_and_hidden() -> None:
    registry = CommandRegistry()
    hits: list[str] = []
    registry.register("run", "desc", lambda: hits.append("x"), aliases=("r",), hidden=True)
    registry.dispatch("r")
    assert hits == ["x"]
    # Hidden commands are excluded from help output.
    assert "run" not in list(registry.help_table().columns[0].cells)


# -- Platform --------------------------------------------------------------
def test_platform_python_interpreter() -> None:
    assert Platform(OperatingSystem.WINDOWS).python == "python"
    assert Platform(OperatingSystem.LINUX).python == "python3"
    assert Platform(OperatingSystem.MACOS).python == "python3"


def test_platform_posix_and_windows_flags() -> None:
    assert Platform(OperatingSystem.LINUX).is_posix
    assert not Platform(OperatingSystem.LINUX).is_windows
    assert Platform(OperatingSystem.WINDOWS).is_windows


# -- CommandRunner ---------------------------------------------------------
def test_runner_dry_run_does_not_execute() -> None:
    runner = CommandRunner(dry_run=True)
    result = runner.run(["definitely-not-a-real-binary", "--flag"])
    assert result.returncode == 0


def test_runner_missing_binary_raises_dependency_error() -> None:
    runner = CommandRunner()
    with pytest.raises(DependencyError):
        runner.run(["definitely-not-a-real-binary-xyz"])


def test_runner_nonzero_exit_raises_tool_error() -> None:
    runner = CommandRunner()
    with pytest.raises(ToolExecutionError):
        runner.run(["python3", "-c", "import sys; sys.exit(3)"])


def test_runner_require_missing_dependency() -> None:
    runner = CommandRunner()
    with pytest.raises(DependencyError):
        runner.require("definitely-not-a-real-binary-xyz")


def test_runner_require_found_dependency() -> None:
    runner = CommandRunner()
    assert runner.require("python3").endswith("python3")
