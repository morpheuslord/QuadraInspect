"""Installer — clone and set up the integrated third-party tools."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from git import GitError, Repo

from quadrainspect.tools.base import OneShotTool, ToolContext


@dataclass(frozen=True)
class ToolRepository:
    """A third-party repository to clone and, optionally, set up."""

    name: str
    url: str
    #: Optional post-clone step; receives the installer and the clone directory.
    post_install: Callable[[Installer, Path], None] | None = field(default=None)


class Installer(OneShotTool):
    """Clone the integrated tools and run their setup steps."""

    name = "installer"
    description = "Download and set up the integrated tools"

    def __init__(self, context: ToolContext) -> None:
        super().__init__(context)
        self._repositories = (
            ToolRepository("andropass", "https://github.com/koengu/AndRoPass"),
            ToolRepository(
                "apkleaks",
                "https://github.com/dwisiswant0/apkleaks",
                post_install=self._setup_apkleaks,
            ),
            ToolRepository(
                "mobfs",
                "https://github.com/MobSF/Mobile-Security-Framework-MobSF.git",
                post_install=self._setup_mobfs,
            ),
            ToolRepository(
                "rms",
                "https://github.com/m0bilesecurity/RMS-Runtime-Mobile-Security",
                post_install=self._setup_rms,
            ),
        )

    def execute(self) -> None:
        self.log.info("Detected operating system: %s", self.platform.os.value)
        self.workspace.ensure_directories()
        for repo in self._repositories:
            self._install(repo)
        self.log.info("Installation complete")

    # -- per-repository steps ---------------------------------------------
    def _install(self, repo: ToolRepository) -> None:
        destination = self.workspace.tool_dir(repo.name)
        self._clone(repo, destination)
        if repo.post_install is not None:
            try:
                repo.post_install(self, destination)
            except Exception as exc:  # noqa: BLE001 - setup is best-effort
                self.log.warning("Setup step for %s failed: %s", repo.name, exc)

    def _clone(self, repo: ToolRepository, destination: Path) -> None:
        if destination.exists():
            self.log.info("%s already present, skipping clone", repo.name)
            return
        self.log.info("Cloning %s", repo.name)
        try:
            Repo.clone_from(repo.url, str(destination))
        except GitError as exc:
            self.log.warning("Could not clone %s: %s", repo.name, exc)

    def _setup_apkleaks(self, _installer: Installer, directory: Path) -> None:
        python = self.platform.python
        self.runner.run([python, "setup.py", "build"], cwd=directory, check=False)
        self.runner.run([python, "setup.py", "install"], cwd=directory, check=False)

    def _setup_mobfs(self, _installer: Installer, directory: Path) -> None:
        if self.platform.is_windows:
            self.runner.run(["cmd", "/c", "setup.bat"], cwd=directory, check=False)
        else:
            self.runner.run(["sudo", "bash", "setup.sh"], cwd=directory, check=False)

    def _setup_rms(self, _installer: Installer, directory: Path) -> None:
        self.runner.run(
            ["npm", "install", "-g", "rms-runtime-mobile-security"],
            cwd=directory,
            check=False,
        )
        self.runner.run(
            ["npm", "install", "express", "nunjucks", "socket.io", "frida", "node-datetime"],
            cwd=directory,
            check=False,
        )
