"""AndroPass integration — analyse APK authentication/authorisation."""
from __future__ import annotations

from quadrainspect.tools.base import InteractiveTool


class AndroPassTool(InteractiveTool):
    """Interactive front-end for the bundled ``AndRoPass`` analyser."""

    name = "andropass"
    description = "Analyse an APK with the AndroPass analyser"
    prompt = "ANDROPASS"
    help_title = "AndroPass Help Menu"

    def register_commands(self) -> None:
        self.registry.register(
            "attack", "Run the AndroPass analysis against the target", self._attack
        )

    def _attack(self) -> None:
        target = self.session.target_path  # raises TargetNotSetError if unset
        script = self.workspace.tool_dir(self.name) / "AndRoPass.py"
        argv = [self.platform.python, str(script), "-a", str(target)]
        self.log.info("Analysing %s with AndroPass", target.name)
        self.runner.run(argv)
