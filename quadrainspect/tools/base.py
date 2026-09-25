"""Base classes and shared context for integrated tools."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from quadrainspect.console import get_logger
from quadrainspect.platform import Platform
from quadrainspect.runner import CommandRunner
from quadrainspect.session import Session, Workspace
from quadrainspect.shell import InteractiveShell


@dataclass(frozen=True)
class ToolContext:
    """Dependencies shared by every tool.

    Passing a single context object (dependency injection) keeps tool
    constructors uniform and makes the tools trivial to test with fakes.
    """

    session: Session
    runner: CommandRunner
    platform: Platform

    @property
    def workspace(self) -> Workspace:
        return self.session.workspace


class Tool(ABC):  # noqa: B024 - abstract base; the execution contract lives on subclasses
    """Common metadata and helpers for all tools.

    Not instantiated directly; use :class:`OneShotTool` or
    :class:`InteractiveTool`, which define the actual execution contract. Being an
    :class:`~abc.ABC` means the ``@abstractmethod`` on :meth:`OneShotTool.execute`
    is genuinely enforced.
    """

    #: Machine-friendly identifier, also used as the on-disk tool directory name.
    name: str = ""
    #: One-line human readable summary shown in listings.
    description: str = ""

    def __init__(self, context: ToolContext) -> None:
        self.context = context
        self.log = get_logger(self.name or self.__class__.__name__)

    @property
    def session(self) -> Session:
        return self.context.session

    @property
    def runner(self) -> CommandRunner:
        return self.context.runner

    @property
    def platform(self) -> Platform:
        return self.context.platform

    @property
    def workspace(self) -> Workspace:
        return self.context.workspace


class OneShotTool(Tool):
    """A tool that runs to completion in a single call."""

    @abstractmethod
    def execute(self) -> None:
        """Perform the tool's action."""


class InteractiveTool(Tool, InteractiveShell):
    """A tool that drives its own interactive sub-menu.

    The class cooperates across both bases: :class:`Tool` stores the shared
    context while :class:`InteractiveShell` builds the command registry and runs
    the REPL. Subclasses implement
    :meth:`~quadrainspect.shell.InteractiveShell.register_commands`.
    """

    def __init__(self, context: ToolContext) -> None:
        Tool.__init__(self, context)
        InteractiveShell.__init__(self)
