"""Workspace layout and runtime session state.

:class:`Workspace` owns the on-disk directory layout (``tools``, ``results``,
``target`` and ``pattern``) and resolves paths relative to the framework root.
:class:`Session` holds the mutable state of a run — chiefly the currently
selected target APK — and exposes it through validated accessors so that tools no
longer have to guess whether a target has been set.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from quadrainspect.exceptions import TargetNotSetError


@dataclass(frozen=True)
class Workspace:
    """Resolved directory layout for a QuadraInspect installation."""

    root: Path

    @classmethod
    def from_path(cls, root: Path | str) -> Workspace:
        """Build a workspace rooted at *root*, resolved to an absolute path."""
        return cls(root=Path(root).expanduser().resolve())

    @property
    def tools_dir(self) -> Path:
        return self.root / "tools"

    @property
    def results_dir(self) -> Path:
        return self.root / "results"

    @property
    def target_dir(self) -> Path:
        return self.root / "target"

    @property
    def pattern_dir(self) -> Path:
        return self.root / "pattern"

    @property
    def config_dir(self) -> Path:
        return self.root / "config"

    @property
    def managed_directories(self) -> tuple[Path, ...]:
        """Directories the framework creates and manages on the user's behalf."""
        return (self.tools_dir, self.results_dir, self.target_dir, self.pattern_dir)

    def ensure_directories(self) -> None:
        """Create every managed directory, ignoring ones that already exist."""
        for directory in self.managed_directories:
            directory.mkdir(parents=True, exist_ok=True)

    def tool_dir(self, name: str) -> Path:
        """Return the install location of an integrated tool named *name*."""
        return self.tools_dir / name


class Session:
    """Mutable per-run state shared between the app and its tools."""

    def __init__(self, workspace: Workspace, *, target: str | None = None) -> None:
        self.workspace = workspace
        self._target = target or None

    @property
    def target(self) -> str | None:
        """The currently selected target APK file name, if any."""
        return self._target

    @target.setter
    def target(self, value: str | None) -> None:
        self._target = value.strip() if value and value.strip() else None

    @property
    def has_target(self) -> bool:
        return self._target is not None

    @property
    def target_path(self) -> Path:
        """Absolute path to the selected target inside the ``target`` directory.

        Raises
        ------
        TargetNotSetError
            If no target has been selected yet.
        """
        if self._target is None:
            raise TargetNotSetError(
                "No target APK selected. Use 'SET target' (frame mode) or "
                "--target (argument mode) first."
            )
        return self.workspace.target_dir / self._target
