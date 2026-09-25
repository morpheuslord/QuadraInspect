"""Add-ins manager — install optional, community-contributed tools.

Add-ons are declared as :class:`AddOn` objects with an ``install`` callable, so
new tools can be contributed by adding an entry to :data:`AddinsManager._addons`
rather than by extending a ``switch`` statement (as the original required).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from git import GitError, Repo
from rich.prompt import Prompt
from rich.table import Table

from quadrainspect.console import console
from quadrainspect.exceptions import UnsupportedPlatformError
from quadrainspect.net import download_file
from quadrainspect.tools.base import InteractiveTool, ToolContext


@dataclass(frozen=True)
class AddOn:
    """An optional tool that can be installed on demand."""

    key: str
    name: str
    os_support: str
    depends: str
    install: Callable[[], None]


class AddinsManager(InteractiveTool):
    """Interactive manager for optional add-on tools."""

    name = "addins"
    description = "Install optional community add-on tools"
    prompt = "Addins Main"
    help_title = "Add-ins Menu"

    # Third-party download locations for the bundled add-ons.
    APKEDITOR_JAR = (
        "https://github.com/REAndroid/APKEditor/releases/download/"
        "V1.1.8/APKEditor-1.1.8.jar"
    )
    BACKDOOR_REPO = "https://github.com/am6539/backdoor-apk-master"
    BAKSMALI_JAR = "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar"
    APKTOOL_JAR = (
        "https://github.com/iBotPeaches/Apktool/releases/download/"
        "v2.7.0/apktool_2.7.0.jar"
    )

    def __init__(self, context: ToolContext) -> None:
        self._addons: dict[str, AddOn] = {}
        super().__init__(context)
        self._register_addons()

    def register_commands(self) -> None:
        self.registry.register("list", "List the available add-ons", self._list, aliases=("help",))
        self.registry.register("install", "Install an add-on by its number", self._install)

    def _register_addons(self) -> None:
        addons = (
            AddOn("1", "APKEditor", "Windows/Linux/macOS", "Java", self._install_apkeditor),
            AddOn("2", "Backdoor-APK", "Linux/macOS (tested on Kali)", "Java", self._install_backdoor),
        )
        self._addons = {addon.key: addon for addon in addons}

    # -- menu commands -----------------------------------------------------
    def _list(self) -> None:
        table = Table(title="Add-ons Menu")
        table.add_column("Number", style="bold cyan")
        table.add_column("Name")
        table.add_column("OS")
        table.add_column("Depends")
        for addon in self._addons.values():
            table.add_row(addon.key, addon.name, addon.os_support, addon.depends)
        console.print(table)

    def _install(self) -> None:
        choice = Prompt.ask("Add-on number to install", choices=list(self._addons))
        addon = self._addons[choice]
        self.log.info("Installing %s", addon.name)
        addon.install()

    # -- individual add-on installers -------------------------------------
    def _install_apkeditor(self) -> None:
        self.runner.require("java", hint="Install a Java runtime environment (JRE).")
        destination = self.workspace.tool_dir("apkeditor") / "apkeditor.jar"
        download_file(self.APKEDITOR_JAR, destination)
        self.log.info("APKEditor installed at %s", destination)

    def _install_backdoor(self) -> None:
        if not self.platform.is_posix:
            raise UnsupportedPlatformError(
                "The Backdoor-APK add-on is only supported on Linux and macOS."
            )
        self.runner.require("java", hint="Install a Java runtime environment (JRE).")
        if self.runner.which("msfconsole") is None:
            self.log.warning(
                "Metasploit (msfconsole) was not found. Install it before running "
                "the backdoor tool: https://www.metasploit.com/"
            )

        root = self.workspace.tool_dir("backdoor-apk-master")
        self._clone_backdoor(root)

        backdoor_dir = root / "backdoor-apk"
        download_file(self.BAKSMALI_JAR, backdoor_dir / "baksmali.jar")
        download_file(self.APKTOOL_JAR, backdoor_dir / "apktool.jar")
        self._mark_executables(backdoor_dir)
        self.log.info("Backdoor-APK installed at %s", backdoor_dir)

    def _clone_backdoor(self, root: Path) -> None:
        # Clone into ``root`` itself so that the repository's ``backdoor-apk``
        # subdirectory lands at ``tools/backdoor-apk-master/backdoor-apk`` — the
        # exact path the jar downloads, chmod step and BackdoorTool all expect.
        if root.exists():
            self.log.info("Backdoor-APK already present, skipping clone")
            return
        try:
            Repo.clone_from(self.BACKDOOR_REPO, str(root))
        except GitError as exc:
            self.log.warning("Could not clone Backdoor-APK: %s", exc)

    def _mark_executables(self, backdoor_dir: Path) -> None:
        """Make third-party helper binaries executable, ignoring absent ones."""
        third_party = backdoor_dir / "third-party"
        candidates = (
            third_party / "android-string-obfuscator" / "lib",
            third_party / "android-sdk-linux" / "build-tools" / "25.0.2",
            third_party / "proguard5.3.2" / "lib",
        )
        for directory in candidates:
            if not directory.is_dir():
                continue
            for entry in directory.iterdir():
                if entry.is_file():
                    entry.chmod(entry.stat().st_mode | 0o111)
