"""Centralised subprocess execution.

Every external command in QuadraInspect is dispatched through
:class:`CommandRunner`. This gives the framework a single place to:

* run commands as argument *lists* (``shell=False``) so that user-supplied
  values such as target file names can never be interpreted by a shell — closing
  the command-injection holes that the original string-formatted ``shell=True``
  calls were exposed to;
* translate low-level :mod:`subprocess` failures into the framework's own
  :class:`~quadrainspect.exceptions.ToolExecutionError` /
  :class:`~quadrainspect.exceptions.DependencyError`;
* discover and require external dependencies via :meth:`which` / :meth:`require`;
* support a ``dry_run`` mode that logs commands without executing them.
"""
from __future__ import annotations

import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

from quadrainspect.console import get_logger
from quadrainspect.exceptions import DependencyError, ToolExecutionError


class CommandRunner:
    """Execute external commands with consistent logging and error handling."""

    def __init__(self, *, dry_run: bool = False) -> None:
        self._log = get_logger("runner")
        self.dry_run = dry_run

    # -- discovery ---------------------------------------------------------
    def which(self, program: str) -> str | None:
        """Return the resolved path to *program*, or ``None`` if not found."""
        return shutil.which(program)

    def require(self, program: str, *, hint: str | None = None) -> str:
        """Return the path to *program* or raise :class:`DependencyError`.

        Parameters
        ----------
        program:
            Executable name to look up on ``PATH``.
        hint:
            Optional guidance appended to the error message telling the user how
            to install the missing dependency.
        """
        resolved = self.which(program)
        if resolved is None:
            message = f"Required dependency {program!r} was not found on PATH."
            if hint:
                message = f"{message} {hint}"
            raise DependencyError(message)
        return resolved

    # -- execution ---------------------------------------------------------
    def run(
        self,
        argv: Sequence[str],
        *,
        cwd: Path | str | None = None,
        check: bool = True,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run *argv* as a non-shell command.

        Parameters
        ----------
        argv:
            The program and its arguments as a sequence of strings.
        cwd:
            Working directory for the child process. The framework never changes
            its own working directory; it passes ``cwd`` instead.
        check:
            When true, a non-zero exit status raises
            :class:`~quadrainspect.exceptions.ToolExecutionError`.
        capture_output:
            When true, capture and return ``stdout``/``stderr`` instead of
            streaming them to the console.

        Returns
        -------
        subprocess.CompletedProcess
            The completed process, with decoded text streams.
        """
        argv = [str(part) for part in argv]
        printable = " ".join(argv)
        if self.dry_run:
            self._log.info("[dim](dry-run)[/] %s", printable)
            return subprocess.CompletedProcess(argv, 0, "", "")

        self._log.debug("Executing: %s", printable)
        try:
            completed = subprocess.run(
                argv,
                cwd=str(cwd) if cwd is not None else None,
                check=check,
                text=True,
                capture_output=capture_output,
            )
        except FileNotFoundError as exc:
            raise DependencyError(
                f"Command not found: {argv[0]!r}. Is it installed and on PATH?"
            ) from exc
        except subprocess.CalledProcessError as exc:
            raise ToolExecutionError(
                f"Command failed with exit code {exc.returncode}: {printable}",
                returncode=exc.returncode,
            ) from exc
        return completed

    def run_script(
        self,
        script: str,
        *,
        cwd: Path | str | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        """Run a *fixed, trusted* shell script string.

        This is reserved for installer pipelines that are constant literals (they
        contain no user-supplied data) but rely on shell features such as pipes
        and ``&&`` chaining. Never pass externally-influenced data here — use
        :meth:`run` with an argument list for anything that includes user input.
        """
        if self.dry_run:
            self._log.info("[dim](dry-run)[/] %s", script)
            return subprocess.CompletedProcess(script, 0, "", "")

        self._log.debug("Executing shell script: %s", script)
        try:
            completed = subprocess.run(
                script,
                cwd=str(cwd) if cwd is not None else None,
                shell=True,  # noqa: S602 - trusted constant scripts only
                check=check,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            raise ToolExecutionError(
                f"Installer step failed with exit code {exc.returncode}.",
                returncode=exc.returncode,
            ) from exc
        return completed
