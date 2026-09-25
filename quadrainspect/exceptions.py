"""Exception hierarchy for QuadraInspect.

Every error the framework raises deliberately derives from
:class:`QuadraInspectError`, which lets the command loop distinguish *expected*
operational failures (a missing dependency, an unset target, a tool that exited
non-zero) from genuine, unexpected bugs. Expected failures are reported to the
user cleanly; anything else is allowed to propagate for a full traceback.
"""
from __future__ import annotations


class QuadraInspectError(Exception):
    """Base class for all errors raised intentionally by the framework."""


class ConfigurationError(QuadraInspectError):
    """Raised when the framework is misconfigured or a path cannot be resolved."""


class UnsupportedPlatformError(ConfigurationError):
    """Raised when the host operating system is not supported."""


class TargetNotSetError(QuadraInspectError):
    """Raised when an operation needs a target APK but none has been selected."""


class DependencyError(QuadraInspectError):
    """Raised when a required external program or tool is not available."""


class ToolExecutionError(QuadraInspectError):
    """Raised when an external tool cannot be launched or exits with an error.

    Parameters
    ----------
    message:
        Human readable description of what failed.
    returncode:
        Exit status of the underlying process when one is available.
    """

    def __init__(self, message: str, *, returncode: int | None = None) -> None:
        super().__init__(message)
        self.returncode = returncode


class CommandError(QuadraInspectError):
    """Raised when an interactive command is unknown or used incorrectly."""
