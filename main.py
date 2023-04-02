import os
import platform
import argparse
from git import Repo
from pyfiglet import Figlet
from subprocess import run
from rich.console import Console
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.table import Table

console = Console()
os.chdir(os.getcwd())
path = str(os.getcwd())
fn = ""

parser = argparse.ArgumentParser(
    description='Python-Nmap and chatGPT intigrated Vulnerability scanner')
parser.add_argument('--target', metavar='target', type=str,
                    help='APK FILE NAME', required=False)

args = parser.parse_args()
target = args.target


def banner():
    f = Figlet(font='slant')
    console.print(f.renderText('AFrame'), style="bold")
    pass


def installer():
    pprint("Validating OS:")
    osp = platform.system()
    pprint("OS FOUND: {}".format(osp))
    command = ""
    cmd_mob = ""
    match osp:
        case 'Darwin':
            command = "python3 setup.py build && python3 setup.py install"
            cmd_mob = "sudo bash setup.sh"
        case 'Linux':
            command = "python3 setup.py build && python3 setup.py install"
            cmd_mob = "sudo bash setup.sh"
        case 'Windows':
            command = "python setup.py build && python setup.py install"
            cmd_mob = ".\setup.bat"
    andropass = 'https://github.com/koengu/AndRoPass'
    apkleaks = 'https://github.com/dwisiswant0/apkleaks'
    mobfs = 'https://github.com/MobSF/Mobile-Security-Framework-MobSF.git'
    try:
        os.makedirs('tools')
    except FileExistsError:
        pass
    try:
        os.makedirs('results')
    except FileExistsError:
        pass
    try:
        os.makedirs('pattern')
    except FileExistsError:
        pass
    try:
        os.makedirs('target')
    except FileExistsError:
        pass
    os.chdir('{}/tools'.format(path))
    twd = os.getcwd()
    pprint("Cloning AndroPass")
    try:
        Repo.clone_from(andropass, '{}/andropass'.format(twd))
    except:
        pass
    pprint("Cloning APKLeaks")
    try:
        Repo.clone_from(apkleaks, '{}/apkleaks'.format(twd))
    except:
        pass
    pprint("Cloning MOBfs")
    try:
        Repo.clone_from(mobfs, '{}/mobfs'.format(twd))
    except:
        pass
    os.chdir('{}/apkleaks'.format(twd))
    run(command, shell=True)
    os.chdir('{}/mobfs'.format(twd))
    run(cmd_mob, shell=True)
    pprint('Install Complete')


def andropass(fn):
    try:
        osp = platform.system()
        p = ""
        match osp:
            case 'Darwin':
                p = "python3"
            case 'Linux':
                p = "python3"
            case 'Windows':
                p = "python"
        rdir = os.getcwd()
        tdir = '{}/tools/andropass/'.format(rdir)
        tfile = '{x}/target/{y}'.format(x=rdir, y=fn)
        while True:
            command = Prompt.ask("ANDROPASS>> ")
            match command:
                case 'attack':
                    run("{a} {b}AndRoPass.py -a {c}".format(a=p, b=tdir, c=tfile))
                case 'help':
                    pprint("This has no more than 1 option")
                    table = Table(title="Tools Intigrated")
                    table.add_column("Command")
                    table.add_column("Details")
                    table.add_row("attack", "To start the attack")
                    table.add_row("quit", "Quit the program")
                    table.add_row("return", "return to the main menu")
                    console.print(table)
                case 'SHOW OPTIONS':
                    pass
                case 'return':
                    main()
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")


def apkleaks(fn):
    outfn = ""
    cargs = ""
    jsono = ""
    rulesj = ""
    try:
        osp = platform.system()
        p = ""
        match osp:
            case 'Darwin':
                p = "python3"
            case 'Linux':
                p = "python3"
            case 'Windows':
                p = "python"
        rdir = os.getcwd()
        tdir = '{}/tools/apkleaks/'.format(rdir)
        tfile = '{x}/target/{y}'.format(x=rdir, y=fn)
        final_cmd = str("")
        while True:
            command = Prompt.ask("APKLEAKS>> ")
            match command:
                case 'SET pattern':
                    promptj = Prompt.ask("Enter Prompt file >>")
                    rulesj = '{a}/pattern/{b}'.format(a=rdir, b=promptj)
                    final_cmd += str(" -p {}".format(rulesj))
                case 'SET output':
                    outfn = Prompt.ask("Enter output file Name >>")
                    ofile = '{a}/results/{b}'.format(a=rdir, b=outfn)
                    final_cmd += str(" -o {}".format(ofile))
                case 'SET json-out':
                    jsono = Prompt.ask("Enter output file Name >>")
                    ojfile = '{a}/results/{b}'.format(a=rdir, b=jsono)
                    final_cmd += str(" --json {}".format(ojfile))
                case 'SET arguments':
                    cargs = Prompt.ask("Enter arguments >>")
                    argn = '{b}'.format(b=cargs)
                    final_cmd += str(" -a {}".format(argn))
                case 'attack':
                    run("{a} {b}apkleaks.py {c} -f {d}".format(a=p,
                        b=tdir, c=final_cmd, d=tfile))
                case 'SHOW OPTIONS':
                    opt = Table(title="Options SET")
                    opt.add_column("OPTION")
                    opt.add_column("SET Value")
                    opt.add_row("OUTPUT FILE", str(outfn))
                    opt.add_row("ARGUMENTS", str(cargs))
                    opt.add_row("JSON OUTPUT", str(jsono))
                    opt.add_row("PATTERN", str(rulesj))
                    console.print(opt)
                case 'help':
                    opt = Table(title="APKLeaks Help Menu")
                    opt.add_column("OPTION")
                    opt.add_column("Discription")
                    opt.add_row("SET output",
                                "Write to file results")
                    opt.add_row("SET arguments", "Disassembler arguments")
                    opt.add_row("SET json-out", "For JSON output")
                    opt.add_row("SET pattern", "custom patterns JSON Rules")
                    opt.add_row("help", "Displays help menu")
                    console.print(opt)
                case 'return':
                    main()
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")


def mobfs(fn):
    try:
        rdir = os.getcwd()
        tdir = '{}/tools/mobfs/'.format(rdir)
        run('{}/run.bat 127.0.0.1:5000'.format(tdir))
        pass
    except KeyboardInterrupt:
        pprint("Ending process ...")


def main():
    command = ""
    fn = target
    banner()
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
                    console.print(table)
                case 'START install_tools':
                    installer()
                case 'START apkleaks':
                    apkleaks(fn)
                case 'START mobfs':
                    mobfs(fn)
                case 'START andropass':
                    andropass(fn)
                case 'SHOW banner':
                    banner()
                case 'help':
                    hm = Table(title="Main Help Menu")
                    hm.add_column("Command")
                    hm.add_column("Details")
                    hm.add_row("SET target", "SET the name of the targetfile")
                    hm.add_row("START install_tools",
                               "If not installed this will install the tools")
                    hm.add_row("LIST tools_name",
                               "List out the Tools Intigrated")
                    hm.add_row("START apkleaks", "Use APKLeaks tool")
                    hm.add_row("START andropass", "Use AndroPass APK analizer")
                    hm.add_row("START mobfs",
                               "Use MOBfs for dynamic and static analysis")
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


if __name__ == "__main__":
    main()
