"""APKLeaks integration — scan an APK for leaked secrets and endpoints."""
from __future__ import annotations

from rich.prompt import Prompt
from rich.table import Table

from quadrainspect.console import console
from quadrainspect.tools.base import InteractiveTool, ToolContext


class ApkLeaksTool(InteractiveTool):
    """Interactive front-end for the bundled ``apkleaks`` scanner."""

    name = "apkleaks"
    description = "Scan an APK for leaked secrets, URIs and endpoints"
    prompt = "APKLEAKS"
    help_title = "APKLeaks Help Menu"

    def __init__(self, context: ToolContext) -> None:
        # Accumulated optional arguments and their display values.
        self._args: list[str] = []
        self._options: dict[str, str] = {}
        super().__init__(context)

    def register_commands(self) -> None:
        self.registry.register(
            "SET output", "Write results to a file in the results directory",
            self._set_output,
        )
        self.registry.register(
            "SET arguments", "Additional disassembler arguments", self._set_arguments
        )
        self.registry.register(
            "SET json-out", "Write JSON results to the results directory",
            self._set_json_output,
        )
        self.registry.register(
            "SET pattern", "Use a custom pattern JSON file from the pattern directory",
            self._set_pattern,
        )
        self.registry.register("SHOW OPTIONS", "Display the configured options", self._show_options)
        self.registry.register("attack", "Run the scan against the target", self._attack)

    # -- option setters ----------------------------------------------------
    def _set_output(self) -> None:
        name = Prompt.ask("Enter output file name")
        path = self.workspace.results_dir / name
        self._args += ["-o", str(path)]
        self._options["OUTPUT FILE"] = name

    def _set_json_output(self) -> None:
        name = Prompt.ask("Enter JSON output file name")
        path = self.workspace.results_dir / name
        self._args += ["--json", str(path)]
        self._options["JSON OUTPUT"] = name

    def _set_arguments(self) -> None:
        extra = Prompt.ask("Enter arguments")
        self._args += ["-a", extra]
        self._options["ARGUMENTS"] = extra

    def _set_pattern(self) -> None:
        name = Prompt.ask("Enter pattern file name")
        path = self.workspace.pattern_dir / name
        self._args += ["-p", str(path)]
        self._options["PATTERN"] = name

    # -- actions -----------------------------------------------------------
    def _show_options(self) -> None:
        table = Table(title="Options SET")
        table.add_column("OPTION", style="bold cyan")
        table.add_column("SET Value")
        table.add_row("TARGET", self.session.target or "[not set]")
        for key, value in self._options.items():
            table.add_row(key, value)
        console.print(table)

    def _attack(self) -> None:
        target = self.session.target_path  # raises TargetNotSetError if unset
        script = self.workspace.tool_dir(self.name) / "apkleaks.py"
        argv = [self.platform.python, str(script), *self._args, "-f", str(target)]
        self.log.info("Scanning %s with APKLeaks", target.name)
        self.runner.run(argv)
