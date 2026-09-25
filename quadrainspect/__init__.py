"""QuadraInspect — a modular Android APK analysis framework.

The package exposes a small, well-factored core (workspace/session state, a
platform abstraction, a subprocess runner and an interactive command registry)
on top of which every integrated tool is implemented as a self-contained class.

Public entry points are kept intentionally small so the framework can be driven
either programmatically or through the :mod:`quadrainspect.cli` command line.
"""
from __future__ import annotations

from quadrainspect.exceptions import (
    CommandError,
    ConfigurationError,
    DependencyError,
    QuadraInspectError,
    TargetNotSetError,
    ToolExecutionError,
    UnsupportedPlatformError,
)

__all__ = [
    "__version__",
    "CommandError",
    "ConfigurationError",
    "DependencyError",
    "QuadraInspectError",
    "TargetNotSetError",
    "ToolExecutionError",
    "UnsupportedPlatformError",
]

__version__ = "2.0.0"
