"""MobFS integration — dynamic and static analysis web service."""
from __future__ import annotations

from quadrainspect.tools.base import OneShotTool


class MobFsTool(OneShotTool):
    """Launch the bundled MobFS analysis service."""

    name = "mobfs"
    description = "Start MobFS for dynamic and static analysis"

    def execute(self) -> None:
        tool_dir = self.workspace.tool_dir(self.name)
        self.log.info("Starting MobFS from %s", tool_dir)
        if self.platform.is_windows:
            argv = ["cmd", "/c", "run.bat"]
        else:
            argv = ["bash", "run.sh"]
        self.runner.run(argv, cwd=tool_dir)
