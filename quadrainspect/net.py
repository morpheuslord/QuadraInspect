"""Small networking helpers.

Downloads use the Python standard library so the framework does not depend on an
external ``wget`` binary being present (as the original scripts did) and behaves
identically across platforms.
"""
from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path

from quadrainspect.console import get_logger
from quadrainspect.exceptions import ToolExecutionError

_log = get_logger("net")


def download_file(url: str, destination: Path) -> Path:
    """Download *url* to *destination*, creating parent directories.

    Raises
    ------
    ToolExecutionError
        If the download cannot be completed.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    _log.info("Downloading %s", url)
    try:
        with urllib.request.urlopen(url) as response, destination.open("wb") as handle:
            handle.write(response.read())
    except (urllib.error.URLError, OSError) as exc:
        raise ToolExecutionError(f"Failed to download {url}: {exc}") from exc
    return destination
