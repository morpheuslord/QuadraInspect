"""APKEditor integration — decompile, build, merge, refactor and protect APKs."""
from __future__ import annotations

from rich.prompt import Prompt
from rich.table import Table

from quadrainspect.console import console
from quadrainspect.exceptions import CommandError
from quadrainspect.tools.base import InteractiveTool, ToolContext


class ApkEditorTool(InteractiveTool):
    """Interactive front-end for the ``APKEditor`` jar.

    APKEditor performs exactly one operation per invocation, so — unlike the
    original which silently concatenated multiple flags — this front-end tracks a
    single pending operation and tells the user when they replace it.
    """

    name = "apkeditor"
    description = "Decompile, build, merge, refactor or protect an APK"
    prompt = "APKEDITOR"
    help_title = "APKEditor Help Menu"

    def __init__(self, context: ToolContext) -> None:
        self._operation: list[str] = []
        self._operation_label: str = "[none]"
        super().__init__(context)

    def register_commands(self) -> None:
        self.registry.register("SET decode", "Decompile the target APK", self._set_decode)
        self.registry.register("SET merge", "Merge split APKs from a directory", self._set_merge)
        self.registry.register("SET build", "Build an APK from a decompiled directory", self._set_build)
        self.registry.register("SET refactor", "Refactor an obfuscated APK", self._set_refactor)
        self.registry.register("SET protect", "Protect an APK against decompilers", self._set_protect)
        self.registry.register("SHOW OPTIONS", "Display the configured options", self._show_options)
        self.registry.register("attack", "Run the configured operation", self._attack)

    # -- helpers -----------------------------------------------------------
    def _output_path(self) -> str:
        return str(self.workspace.results_dir / self.session.target_path.name)

    def _set_operation(self, label: str, args: list[str]) -> None:
        if self._operation:
            self.log.warning(
                "Replacing previously configured operation %r with %r "
                "(APKEditor runs one operation at a time).",
                self._operation_label,
                label,
            )
        self._operation = args
        self._operation_label = label

    # -- option setters ----------------------------------------------------
    def _set_decode(self) -> None:
        target = self.session.target_path
        self._set_operation("decode", ["d", "-i", str(target), "-o", self._output_path()])

    def _set_refactor(self) -> None:
        target = self.session.target_path
        self._set_operation("refactor", ["x", "-i", str(target), "-o", self._output_path()])

    def _set_protect(self) -> None:
        target = self.session.target_path
        self._set_operation("protect", ["p", "-i", str(target), "-o", self._output_path()])

    def _set_merge(self) -> None:
        location = Prompt.ask("Target directory location")
        self._set_operation("merge", ["m", "-i", location])

    def _set_build(self) -> None:
        location = Prompt.ask("Target directory location")
        self._set_operation("build", ["b", "-i", location])

    # -- actions -----------------------------------------------------------
    def _show_options(self) -> None:
        table = Table(title="Options SET")
        table.add_column("OPTION", style="bold cyan")
        table.add_column("SET Value")
        table.add_row("TARGET", self.session.target or "[not set]")
        table.add_row("OPERATION", self._operation_label)
        console.print(table)

    def _attack(self) -> None:
        if not self._operation:
            raise CommandError(
                "No operation configured. Use one of the 'SET' commands first."
            )
        jar = self.workspace.tool_dir(self.name) / "apkeditor.jar"
        argv = [*self.platform.java, str(jar), *self._operation]
        self.log.info("Running APKEditor '%s' operation", self._operation_label)
        self.runner.run(argv)
