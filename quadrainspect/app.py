"""Application orchestrator.

:class:`QuadraInspect` wires the core services together and exposes the two ways
the framework can be driven:

* *frame* mode — an interactive main menu (:class:`MainShell`); and
* *argument* mode — a single command executed non-interactively.

Both modes are driven by the **same** list of :class:`MenuEntry` objects, so the
main menu and its argument-mode equivalent can never drift apart the way the two
duplicated ``match`` blocks in the original ``main.py`` did.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from rich.prompt import Prompt
from rich.table import Table

from quadrainspect.console import console, get_logger, render_banner
from quadrainspect.exceptions import CommandError
from quadrainspect.platform import Platform
from quadrainspect.runner import CommandRunner
from quadrainspect.session import Session, Workspace
from quadrainspect.shell import InteractiveShell, QuitProgram
from quadrainspect.tools import (
    AddinsManager,
    AddinsUpdater,
    AndroPassTool,
    ApkEditorTool,
    ApkLeaksTool,
    BackdoorTool,
    FullInstaller,
    Installer,
    MobFsTool,
    RmsTool,
    ToolContext,
)


@dataclass(frozen=True)
class MenuEntry:
    """A single main-menu action, shared between frame and argument modes.

    Attributes
    ----------
    frame_name:
        Command string used in interactive frame mode (``None`` to hide it there).
    arg_name:
        Command string accepted by ``--command`` in argument mode (``None`` to
        hide it there — e.g. interactive-only actions).
    description:
        Help text shown in both modes.
    action:
        The zero-argument callable invoked when the entry is selected.
    """

    frame_name: str | None
    arg_name: str | None
    description: str
    action: Callable[[], None]


class QuadraInspect:
    """Top-level application object."""

    def __init__(
        self,
        workspace: Workspace,
        *,
        target: str | None = None,
        dry_run: bool = False,
    ) -> None:
        self._log = get_logger("app")
        self.session = Session(workspace, target=target)
        self.platform = Platform.current()
        self.runner = CommandRunner(dry_run=dry_run)
        self.context = ToolContext(
            session=self.session, runner=self.runner, platform=self.platform
        )
        self.entries = self._build_menu()

    # -- menu construction -------------------------------------------------
    def _build_menu(self) -> list[MenuEntry]:
        return [
            MenuEntry("SET target", None, "Set the target APK file name", self._set_target),
            MenuEntry("LIST tools_name", "tools_name", "List the integrated tools", self._list_tools),
            MenuEntry("START install_tools", "install_tools", "Download and set up the integrated tools", self._run(Installer)),
            MenuEntry("START full_install", "full-install", "Install all tools and add-ons at once", self._run(FullInstaller)),
            MenuEntry("START apkleaks", "apkleaks", "Use the APKLeaks scanner", self._run(ApkLeaksTool)),
            MenuEntry("START andropass", "andropass", "Use the AndroPass analyser", self._run(AndroPassTool)),
            MenuEntry("START backdoor", "backdoor", "Inject a payload into an APK (authorised testing)", self._run(BackdoorTool)),
            MenuEntry("START mobfs", "mobfs", "Use MobFS for dynamic and static analysis", self._run(MobFsTool)),
            MenuEntry("START rms", "rms", "Use RMS for runtime analysis", self._run(RmsTool)),
            MenuEntry("START apkeditor", "apkeditor", "Decompile/build/refactor an APK", self._run(ApkEditorTool)),
            MenuEntry("START addins", "addins", "Install optional add-on tools", self._run(AddinsManager)),
            MenuEntry("update addins", "update-addins", "Update the framework and add-ins", self._run(AddinsUpdater)),
            MenuEntry("SHOW banner", "banner", "Render the banner", render_banner),
        ]

    def _run(self, tool_cls) -> Callable[[], None]:
        """Return a callable that instantiates and launches *tool_cls*.

        Interactive tools expose ``run`` (a REPL); one-shot tools expose
        ``execute``. The correct entry point is chosen automatically.
        """

        def launch() -> None:
            tool = tool_cls(self.context)
            runner = getattr(tool, "run", None) or tool.execute
            runner()

        return launch

    # -- built-in actions --------------------------------------------------
    def _set_target(self) -> None:
        self.session.target = Prompt.ask("Target APK file name")
        self._log.info("Target set to %s", self.session.target)

    def _list_tools(self) -> None:
        table = Table(title="Integrated Tools")
        table.add_column("Number", style="bold cyan")
        table.add_column("Name")
        for index, tool in enumerate(
            (ApkLeaksTool, MobFsTool, AndroPassTool, RmsTool, ApkEditorTool, BackdoorTool),
            start=1,
        ):
            table.add_row(str(index), tool.name)
        console.print(table)

    # -- entry points ------------------------------------------------------
    def run_frame(self) -> None:
        """Run the interactive main menu."""
        self.session.workspace.ensure_directories()
        render_banner()
        try:
            MainShell(self).run()
        except QuitProgram:
            console.print("Happy hacking...")

    def run_argument(self, command: str) -> None:
        """Execute a single *command* in argument mode.

        Raises
        ------
        CommandError
            If *command* does not map to a known argument-mode action.
        """
        self.session.workspace.ensure_directories()
        for entry in self.entries:
            if entry.arg_name == command:
                entry.action()
                return
        raise CommandError(f"Unknown command: {command!r}")

    def argument_help(self) -> Table:
        """Build the argument-mode help table."""
        table = Table(title="Argument Mode Commands")
        table.add_column("Command", style="bold cyan")
        table.add_column("Description")
        for entry in self.entries:
            if entry.arg_name:
                table.add_row(entry.arg_name, entry.description)
        return table


class MainShell(InteractiveShell):
    """The interactive main menu."""

    prompt = "QuadraInspect Main"
    help_title = "Main Help Menu"

    def __init__(self, app: QuadraInspect) -> None:
        self._app = app
        super().__init__()

    def register_commands(self) -> None:
        for entry in self._app.entries:
            if entry.frame_name:
                self.registry.register(entry.frame_name, entry.description, entry.action)
