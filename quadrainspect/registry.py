"""Command registry — the framework's arbitration layer.

The original code decided what to do with a user's input using large
``match``/``case`` (effectively ``switch``) blocks duplicated across every
module, with the help text hand-maintained separately and prone to drifting out
of sync. This module replaces that pattern with a small registry: each command is
a first-class :class:`Command` object bound to a handler, and dispatch plus help
rendering are derived from the same source of truth.
"""
from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass

from rich.table import Table

from quadrainspect.exceptions import CommandError

#: A command handler takes no arguments and returns nothing; it closes over any
#: state it needs (session, runner, ...) at registration time.
Handler = Callable[[], None]


@dataclass(frozen=True)
class Command:
    """A single named command and the handler invoked when it is dispatched."""

    name: str
    description: str
    handler: Handler
    hidden: bool = False
    aliases: tuple[str, ...] = ()


class CommandRegistry:
    """An ordered collection of commands with dispatch and help rendering."""

    def __init__(self) -> None:
        self._commands: list[Command] = []
        self._by_name: dict[str, Command] = {}

    def register(
        self,
        name: str,
        description: str,
        handler: Handler,
        *,
        hidden: bool = False,
        aliases: tuple[str, ...] = (),
    ) -> Command:
        """Register a command and return it.

        Raises
        ------
        CommandError
            If *name* or one of *aliases* is already registered.
        """
        command = Command(
            name=name,
            description=description,
            handler=handler,
            hidden=hidden,
            aliases=aliases,
        )
        for key in (name, *aliases):
            if key in self._by_name:
                raise CommandError(f"Duplicate command registration: {key!r}")
            self._by_name[key] = command
        self._commands.append(command)
        return command

    def __contains__(self, name: str) -> bool:
        return name in self._by_name

    def __iter__(self) -> Iterator[Command]:
        return iter(self._commands)

    def get(self, name: str) -> Command | None:
        """Return the command registered under *name*/alias, or ``None``."""
        return self._by_name.get(name)

    def dispatch(self, name: str) -> None:
        """Invoke the handler registered for *name*.

        Raises
        ------
        CommandError
            If no command is registered under *name*.
        """
        command = self._by_name.get(name)
        if command is None:
            raise CommandError(f"Unknown command: {name!r}")
        command.handler()

    def help_table(self, title: str = "Help Menu") -> Table:
        """Build a rich help :class:`~rich.table.Table` from visible commands."""
        table = Table(title=title)
        table.add_column("Command", style="bold cyan", no_wrap=True)
        table.add_column("Description")
        for command in self._commands:
            if command.hidden:
                continue
            table.add_row(command.name, command.description)
        return table
