import os
import argparse
from pyfiglet import Figlet
from subprocess import run
from rich.console import Console
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.table import Table
from config.installer import installer
from config.androp import androp
from config.apkleaks import apkleaks
from config.mobfs import mobfs
from config.rms import rms

console = Console()
os.chdir(os.getcwd())
path = str(os.getcwd())
fn = ""

parser = argparse.ArgumentParser(
    description='AFrame a APK analysis framework..')
parser.add_argument('--target', metavar='target', type=str,
                    help='APK FILE NAME', required=False)

parser.add_argument('--mode', metavar='mode', type=str,
                    help='Mode of the framework. (frame / argm)', required=False, default='frame')

parser.add_argument('--command', metavar='command', type=str,
                    help='Type of scan you want to continue', required=False)

args = parser.parse_args()
target = args.target
command = args.command
mode = args.mode


def banner():
    f = Figlet(font='slant')
    console.print(f.renderText('AFrame'), style="bold")
    pass


def main():
    command = ""
    fn = target
    banner()
    rdir = os.getcwd()
    match mode:
        case 'frame':
            try:
                while True:
                    command = Prompt.ask("AFrame Main>> ")
                    match command:
                        case 'SET target':
                            fn = Prompt.ask("Name >>")
                        case 'LIST tools_name':
                            table = Table(title="Tools Intigrated")
                            table.add_column("Number")
                            table.add_column("Name")
                            table.add_row("1", "apkleaks")
                            table.add_row("2", "mobfs")
                            table.add_row("3", "andropass")
                            table.add_row("4", "RMS")
                            console.print(table)
                        case 'START install_tools':
                            installer(rdir)
                        case 'START apkleaks':
                            apkleaks(fn, rdir)
                        case 'START mobfs':
                            mobfs(rdir)
                        case 'START rms':
                            rms(rdir)
                        case 'START andropass':
                            androp(fn, rdir)
                        case 'SHOW banner':
                            banner()
                        case 'help':
                            hm = Table(title="Main Help Menu")
                            hm.add_column("Command")
                            hm.add_column("Details")
                            hm.add_row(
                                "SET target", "SET the name of the targetfile")
                            hm.add_row("START install_tools",
                                       "If not installed this will install the tools")
                            hm.add_row("LIST tools_name",
                                       "List out the Tools Intigrated")
                            hm.add_row("START apkleaks", "Use APKLeaks tool")
                            hm.add_row("START andropass",
                                       "Use AndroPass APK analizer")
                            hm.add_row("START mobfs",
                                       "Use MOBfs for dynamic and static analysis")
                            hm.add_row("START rms",
                                       "Use rms for static analysis")
                            hm.add_row("help", "View this current Help menu")
                            hm.add_row("SHOW banner", "Render Banner")
                            hm.add_row("quit", "Quit the Program")
                            console.print(hm)
                        case 'quit':
                            pprint("Happy hacking..")
                            quit()
            except KeyboardInterrupt:
                pprint("I am Quiting!")
                quit()
        case 'argm':
            try:
                match command:
                    case 'SET target':
                        fn = Prompt.ask("Name >>")
                    case 'LIST tools_name':
                        table = Table(title="Tools Intigrated")
                        table.add_column("Number")
                        table.add_column("Name")
                        table.add_row("1", "apkleaks")
                        table.add_row("2", "mobfs")
                        table.add_row("3", "andropass")
                        table.add_row("4", "RMS")
                        console.print(table)
                    case 'START install_tools':
                        installer(rdir)
                    case 'START apkleaks':
                        apkleaks(fn, rdir)
                    case 'START mobfs':
                        mobfs(rdir)
                    case 'START rms':
                        rms(rdir)
                    case 'START andropass':
                        androp(fn, rdir)
                    case 'SHOW banner':
                        banner()
                    case 'help':
                        hm = Table(title="Main Help Menu")
                        hm.add_column("Command")
                        hm.add_column("Details")
                        hm.add_row(
                            "SET target", "SET the name of the targetfile")
                        hm.add_row("START install_tools",
                                   "If not installed this will install the tools")
                        hm.add_row("LIST tools_name",
                                   "List out the Tools Intigrated")
                        hm.add_row("START apkleaks", "Use APKLeaks tool")
                        hm.add_row("START andropass",
                                   "Use AndroPass APK analizer")
                        hm.add_row("START mobfs",
                                   "Use MOBfs for dynamic and static analysis")
                        hm.add_row("START rms",
                                   "Use rms for static analysis")
                        hm.add_row("help", "View this current Help menu")
                        console.print(hm)
            except KeyboardInterrupt:
                pprint("I am Quiting!")
                quit()


if __name__ == "__main__":
    main()
