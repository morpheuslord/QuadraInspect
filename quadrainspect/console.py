"""Shared console, logging and banner helpers.

A single :class:`rich.console.Console` instance is shared across the framework so
that all output (tables, prompts, log records) is rendered consistently. Logging
is routed through :class:`rich.logging.RichHandler`, replacing the scattered
``pprint``/``print`` calls of the original code with a single, level-aware
logger.
"""
from __future__ import annotations

import logging

from pyfiglet import Figlet
from rich.console import Console
from rich.logging import RichHandler

#: Process-wide console. Import this rather than constructing new consoles so
#: that width detection, theming and redirection stay consistent everywhere.
console: Console = Console()

_LOGGER_NAME = "quadrainspect"
_CONFIGURED = False


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the framework logger to render through the shared console.

    The call is idempotent: repeated invocations only adjust the log level so
    that, for example, ``--verbose`` can be honoured without stacking handlers.
    """
    global _CONFIGURED
    logger = logging.getLogger(_LOGGER_NAME)
    if not _CONFIGURED:
        handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
        _CONFIGURED = True
    logger.setLevel(level)


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a child of the framework logger.

    Parameters
    ----------
    name:
        Optional sub-component name (for example a tool name). When omitted the
        root framework logger is returned.
    """
    if name:
        return logging.getLogger(f"{_LOGGER_NAME}.{name}")
    return logging.getLogger(_LOGGER_NAME)


def render_banner(font: str = "slant") -> None:
    """Render the QuadraInspect ASCII banner to the shared console."""
    figlet = Figlet(font=font)
    console.print(figlet.renderText("QuadraInspect"), style="bold cyan")
