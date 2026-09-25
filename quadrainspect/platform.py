"""Operating-system abstraction.

The original framework repeated a ``match platform.system()`` block in almost
every module to decide which Python interpreter or launcher to use. That logic
is consolidated here into a single :class:`Platform` value object so callers ask
for *what they need* (the Python interpreter, the Java launcher, ...) rather than
re-deriving it from the OS name each time.
"""
from __future__ import annotations

import platform as _platform
from dataclasses import dataclass
from enum import Enum

from quadrainspect.exceptions import UnsupportedPlatformError


class OperatingSystem(Enum):
    """Supported host operating systems."""

    LINUX = "Linux"
    MACOS = "Darwin"
    WINDOWS = "Windows"

    @classmethod
    def detect(cls) -> OperatingSystem:
        """Detect the current operating system.

        Raises
        ------
        UnsupportedPlatformError
            If the host OS is not one QuadraInspect knows how to drive.
        """
        name = _platform.system()
        try:
            return cls(name)
        except ValueError as exc:  # pragma: no cover - depends on host
            raise UnsupportedPlatformError(
                f"Unsupported operating system: {name!r}"
            ) from exc


@dataclass(frozen=True)
class Platform:
    """Resolved, platform-specific command details.

    Instances are immutable and cheap to pass around. Use :meth:`current` to
    build one for the running host.
    """

    os: OperatingSystem

    @classmethod
    def current(cls) -> Platform:
        """Build a :class:`Platform` describing the current host."""
        return cls(os=OperatingSystem.detect())

    @property
    def is_windows(self) -> bool:
        return self.os is OperatingSystem.WINDOWS

    @property
    def is_posix(self) -> bool:
        return self.os in (OperatingSystem.LINUX, OperatingSystem.MACOS)

    @property
    def python(self) -> str:
        """Name of the Python interpreter to invoke bundled tool scripts with."""
        return "python" if self.is_windows else "python3"

    @property
    def java(self) -> list[str]:
        """Argument prefix used to launch a runnable ``.jar`` file."""
        return ["java", "-jar"]

    @property
    def requires_privilege_escalation(self) -> bool:
        """Whether POSIX tools in this framework typically need ``sudo``."""
        return self.is_posix
