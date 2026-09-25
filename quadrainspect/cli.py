"""Command-line interface for QuadraInspect."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from quadrainspect import __version__
from quadrainspect.app import QuadraInspect
from quadrainspect.console import configure_logging, console, get_logger
from quadrainspect.exceptions import QuadraInspectError
from quadrainspect.session import Workspace

_FRAME_ALIASES = {"frame", "f"}
_ARGUMENT_ALIASES = {"argm", "a", "args", "argument"}


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    parser = argparse.ArgumentParser(
        prog="quadrainspect",
        description="QuadraInspect — an Android APK analysis framework.",
    )
    parser.add_argument("--target", metavar="APK", help="Target APK file name")
    parser.add_argument(
        "--mode",
        default="frame",
        help="Framework mode: 'frame' (interactive) or 'argm' (argument)",
    )
    parser.add_argument(
        "--command",
        help="Command to run in argument mode (see 'help')",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Framework root directory (defaults to the current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Log commands without executing them",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose (debug) logging",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(logging.DEBUG if args.verbose else logging.INFO)
    log = get_logger("cli")

    workspace = Workspace.from_path(args.root)
    mode = args.mode.strip().lower()

    try:
        app = QuadraInspect(workspace, target=args.target, dry_run=args.dry_run)
        if mode in _FRAME_ALIASES:
            app.run_frame()
        elif mode in _ARGUMENT_ALIASES:
            if not args.command:
                console.print(app.argument_help())
                return 0
            app.run_argument(args.command)
        else:
            parser.error(f"Unknown mode: {args.mode!r} (choose 'frame' or 'argm')")
    except QuadraInspectError as exc:
        log.error("%s", exc)
        return 1
    except KeyboardInterrupt:
        console.print()
        log.info("Interrupted. Quitting.")
        return 130
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
