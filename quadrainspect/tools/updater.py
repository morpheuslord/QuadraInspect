"""Updater — refresh the framework from its git repository.

The original updater deleted and re-downloaded a single ``config`` module from a
hard-coded raw URL. Now that the tools ship as an installable package, updating
means pulling the latest revision of the whole framework, which this tool does
via git.
"""
from __future__ import annotations

from git import GitError, Repo
from git.exc import InvalidGitRepositoryError

from quadrainspect.exceptions import ToolExecutionError
from quadrainspect.tools.base import OneShotTool


class AddinsUpdater(OneShotTool):
    """Update the framework to the latest revision using git."""

    name = "updater"
    description = "Update QuadraInspect and its add-ins from git"

    def execute(self) -> None:
        root = self.workspace.root
        try:
            repo = Repo(str(root))
        except InvalidGitRepositoryError as exc:
            raise ToolExecutionError(
                f"{root} is not a git repository; cannot self-update."
            ) from exc

        if repo.bare:
            raise ToolExecutionError("Cannot update a bare repository.")

        self.log.info("Updating QuadraInspect from %s", root)
        try:
            repo.remotes.origin.pull()
        except (GitError, AttributeError) as exc:
            raise ToolExecutionError(f"Update failed: {exc}") from exc
        self.log.info("Update complete")
