"""RMS integration — Runtime Mobile Security instrumentation server."""
from __future__ import annotations

from quadrainspect.tools.base import OneShotTool


class RmsTool(OneShotTool):
    """Launch the bundled RMS (Runtime Mobile Security) server."""

    name = "rms"
    description = "Start the RMS runtime mobile security server"

    #: Default address the RMS web interface binds to.
    default_bind = "127.0.0.1:5000"

    def __init__(self, context, *, bind: str | None = None) -> None:
        super().__init__(context)
        self.bind = bind or self.default_bind

    def execute(self) -> None:
        tool_dir = self.workspace.tool_dir(self.name)
        self.log.info("Starting RMS on %s", self.bind)
        self.runner.run(["node", "rms.js", self.bind], cwd=tool_dir)
