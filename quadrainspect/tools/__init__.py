"""Integrated analysis tools.

Each module in this package wraps one external tool (APKLeaks, MobSF, RMS,
AndroPass, the backdoor generator, APKEditor) or a framework service (installer,
add-ins manager, updater) behind a small class with a uniform interface.
"""
from __future__ import annotations

from quadrainspect.tools.addins import AddinsManager
from quadrainspect.tools.andropass import AndroPassTool
from quadrainspect.tools.apkeditor import ApkEditorTool
from quadrainspect.tools.apkleaks import ApkLeaksTool
from quadrainspect.tools.backdoor import BackdoorTool
from quadrainspect.tools.base import InteractiveTool, OneShotTool, Tool, ToolContext
from quadrainspect.tools.installer import Installer
from quadrainspect.tools.mobfs import MobFsTool
from quadrainspect.tools.rms import RmsTool
from quadrainspect.tools.updater import AddinsUpdater

__all__ = [
    "AddinsManager",
    "AddinsUpdater",
    "AndroPassTool",
    "ApkEditorTool",
    "ApkLeaksTool",
    "BackdoorTool",
    "Installer",
    "InteractiveTool",
    "MobFsTool",
    "OneShotTool",
    "RmsTool",
    "Tool",
    "ToolContext",
]
