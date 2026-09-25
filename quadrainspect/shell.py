"""Interactive shell base class.

:class:`InteractiveShell` provides the read-eval-print loop that every
interactive menu in QuadraInspect shares. Subclasses only declare their commands
in :meth:`register_commands`; the base class owns prompting, dispatch, help,
graceful exit and — crucially — turning expected framework errors into clean
messages instead of letting them tear down the whole session.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from rich.prompt import Prompt

from quadrainspect.console import console, get_logger
from quadrainspect.exceptions import CommandError, QuadraInspectError
from quadrainspect.registry import CommandRegistry


class ExitShell(Exception):
    """Internal signal: leave the current shell and return to its parent."""


class QuitProgram(Exception):
    """Internal signal: quit QuadraInspect entirely."""


class InteractiveShell(ABC):
    """Base class implementing a command-dispatch REPL."""

    #: Text shown at the prompt, e.g. ``"QuadraInspect Main"``.
    prompt: str = "QuadraInspect"
    #: Title used for the auto-generated help table.
    help_title: str = "Help Menu"

    def __init__(self) -> None:
        self._log = get_logger(self.__class__.__name__)
        self.registry = CommandRegistry()
        self.register_commands()
        self._register_builtins()

    # -- subclass hook -----------------------------------------------------
    @abstractmethod
    def register_commands(self) -> None:
        """Register the shell's commands on ``self.registry``."""

    # -- built-ins ---------------------------------------------------------
    def _register_builtins(self) -> None:
        if "help" not in self.registry:
            self.registry.register("help", "Display this help menu", self._show_help)
        if "return" not in self.registry:
            self.registry.register(
                "return", "Return to the previous menu", self._return
            )
        if "quit" not in self.registry:
            self.registry.register("quit", "Quit QuadraInspect", self._quit)

    def _show_help(self) -> None:
        console.print(self.registry.help_table(self.help_title))

    def _return(self) -> None:
        raise ExitShell

    def _quit(self) -> None:
        raise QuitProgram

    # -- main loop ---------------------------------------------------------
    def run(self) -> None:
        """Run the REPL until the user returns, quits, or sends EOF/Ctrl-C."""
        while True:
            try:
                raw = Prompt.ask(f"{self.prompt}>> ")
            except (KeyboardInterrupt, EOFError):
                console.print()
                self._log.info("Leaving %s", self.prompt)
                return

            command = raw.strip()
            if not command:
                continue

            try:
                self.registry.dispatch(command)
            except ExitShell:
                return
            except CommandError:
                self._log.warning(
                    "Unknown command: %s (type 'help' for options)", command
                )
            except QuadraInspectError as exc:
                self._log.error("%s", exc)
