"""Backdoor-APK integration — payload injection for authorised testing.

This wraps the third-party ``backdoor-apk`` shell tool. It is intended solely for
authorised penetration testing and security research against applications you own
or have explicit permission to assess.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from quadrainspect.exceptions import UnsupportedPlatformError
from quadrainspect.tools.base import InteractiveTool


class BackdoorTool(InteractiveTool):
    """Interactive front-end for the bundled ``backdoor-apk`` tool (POSIX only)."""

    name = "backdoor"
    description = "Inject a payload into an APK (authorised testing only)"
    prompt = "backdoor"
    help_title = "Backdoor Help Menu"

    @property
    def _tool_root(self) -> Path:
        return self.workspace.tool_dir("backdoor-apk-master") / "backdoor-apk"

    @property
    def _output_dir(self) -> Path:
        return self.workspace.results_dir / self.session.target_path.name

    def register_commands(self) -> None:
        self.registry.register("attack", "Inject the payload into the target", self._attack)
        self.registry.register("SHOW OPTIONS", "Display the configured options", self._show_options)

    def _show_options(self) -> None:
        from rich.table import Table

        from quadrainspect.console import console

        table = Table(title="Options SET")
        table.add_column("OPTION", style="bold cyan")
        table.add_column("SET Value")
        table.add_row("TARGET", self.session.target or "[not set]")
        table.add_row("OUTPUT", str(self._output_dir) if self.session.has_target else "[not set]")
        console.print(table)

    def _attack(self) -> None:
        if not self.platform.is_posix:
            raise UnsupportedPlatformError(
                "The backdoor tool is only supported on Linux and macOS."
            )
        target = self.session.target_path  # raises TargetNotSetError if unset
        output_dir = self._output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        script = self._tool_root / "backdoor-apk.sh"
        self.log.info("Injecting payload into %s", target.name)
        self.runner.run(["sudo", "bash", str(script), str(target)], cwd=self._tool_root)
        self._collect_artifacts(output_dir)

    def _collect_artifacts(self, output_dir: Path) -> None:
        """Copy generated artifacts into the per-target results directory."""
        produced_dir = self._tool_root / "out"
        produced_rc = self._tool_root / "backdoor-apk.rc"
        if produced_dir.is_dir():
            shutil.copytree(produced_dir, output_dir / "out", dirs_exist_ok=True)
        if produced_rc.is_file():
            shutil.copy2(produced_rc, output_dir)
        self.log.info("Artifacts collected in %s", output_dir)
