"""Complete installer — set up every integrated tool and add-on in one step.

This is a convenience wrapper for users who want a single "install everything"
action instead of running ``install_tools`` and then each add-on by hand. It runs
the standard :class:`~quadrainspect.tools.installer.Installer` and then installs
all add-ons best-effort (see :meth:`AddinsManager.install_all`).
"""
from __future__ import annotations

from quadrainspect.tools.addins import AddinsManager
from quadrainspect.tools.base import OneShotTool
from quadrainspect.tools.installer import Installer


class FullInstaller(OneShotTool):
    """Install the integrated tools and every add-on in a single run."""

    name = "full-installer"
    description = "Install all integrated tools and add-ons at once"

    def execute(self) -> None:
        self.log.info("Starting complete installation")
        self.workspace.ensure_directories()

        self.log.info("Step 1/2: integrated tools")
        Installer(self.context).execute()

        self.log.info("Step 2/2: optional add-ons")
        AddinsManager(self.context).install_all()

        self.log.info("Complete installation finished")
