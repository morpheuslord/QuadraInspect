import os
import platform
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


def banner():
    f = Figlet(font='slant')
    console.print(f.renderText('AFrame'), style="bold")
    pass


def installer():
    pprint("Validating OS:")
    osp = platform.system()
    pprint("OS FOUND: {}".format(osp))
    command = ""
    match osp:
        case 'Darwin':
            command = "python3 setup.py build && python3 setup.py install"
        case 'Linux':
            command = "python3 setup.py build && python3 setup.py install"
        case 'Windows':
            command = "python setup.py build && python setup.py install"
    andropass = 'https://github.com/koengu/AndRoPass'
    apkleaks = 'https://github.com/dwisiswant0/apkleaks'
    apkutil = 'https://github.com/aktsk/apkutil'
    try:
        os.makedirs('tools')
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
    pprint("Cloning APKUtil")
    try:
        Repo.clone_from(apkutil, '{}/apkutil'.format(twd))
    except:
        pass
    os.chdir('{}/apkleaks'.format(twd))
    run(command, shell=True)
    os.chdir('{}/apkutil'.format(twd))
    run(command, shell=True)
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
        final_cmd = ""
        tfile = '{x}/target/{y}'.format(x=rdir, y=fn)
        while True:
            command = Prompt.ask("APKLEAKS>> ")
            match command:
                case 'SET pattern':
                    promptj = Prompt.ask("Enter Prompt file >>")
                    rulesj = '{a}/rule/{b}'.format(a=rdir, b=promptj)
                    final_cmd += " -p {}".format(rulesj)
                case 'SET output':
                    outfn = Prompt.ask("Enter output file Name >>")
                    ofile = '{a}/results/{b}'.format(a=rdir, b=outfn)
                    final_cmd += " -o {}".format(ofile)
                case 'SET json-out':
                    jsono = Prompt.ask("Enter output file Name >>")
                    ojfile = '{a}/results/{b}'.format(a=rdir, b=jsono)
                    final_cmd += " --json {}".format(ojfile)
                case 'SET arguments':
                    cargs = Prompt.ask("Enter arguments >>")
                    argn = '{b}'.format(b=cargs)
                    final_cmd += " -a {}".format(argn)
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
                    opt.add_row("OUTPUT FILE",
                                "Write to file results")
                    opt.add_row("ARGUMENTS", "Disassembler arguments")
                    opt.add_row("JSON OUTPUT", "For JSON output")
                    opt.add_row("PATTERN", "custom patterns JSON Rules")
                    console.print(opt)
                case 'return':
                    main()
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")


def apkutil(fn):
    all = False
    debuggable = False
    network = False
    info = False
    screenshot = False
    decode = False
    build = False
    sign = False
    align = False
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
        acmd = ""
        tdir = '{}/.venv/Scripts/'.format(rdir)
        tfile = '{x}/target/{y}'.format(x=rdir, y=fn)
        while True:
            command = Prompt.ask("APKUTIL>> ")
            match command:
                case 'SET-ALL':
                    all = True
                    acmd += " all "
                case 'SET-debug':
                    all = False
                    debuggable = True
                    acmd += " d "
                case 'SET-network':
                    all = False
                    network = True
                    acmd += " n "
                case 'SET-info':
                    all = False
                    info = True
                    acmd += " i "
                case 'SET-screenshot':
                    all = False
                    screenshot = True
                    acmd += " ss "
                case 'SET-decode':
                    all = False
                    decode = True
                    acmd += " d "
                case 'SET-build':
                    all = False
                    build = True
                    acmd += " b "
                case 'SET-sign':
                    all = False
                    sign = True
                    acmd += " s "
                case 'SET-align':
                    all = False
                    align = True
                    acmd += " a "
                case 'attack':
                    try:
                        run("apkutil{c} {d}".format(c=acmd, d=tfile))
                    except:
                        print("Installation Error")
                case 'SHOW OPTIONS':
                    opt = Table(title="Options SET")
                    opt.add_column("OPTION")
                    opt.add_column("SET Value")
                    opt.add_row("ALL", str(all))
                    opt.add_row("DEBUGABLE", str(debuggable))
                    opt.add_row("NETWORK", str(network))
                    opt.add_row("INFO", str(info))
                    opt.add_row("SCREENSHOT", str(screenshot))
                    opt.add_row("DECODE", str(decode))
                    opt.add_row("BUILD", str(build))
                    opt.add_row("SIGN", str(sign))
                    opt.add_row("ALIGN", str(align))
                    console.print(opt)
                case 'help':
                    opt = Table(title="APKUtil Help menu")
                    opt.add_column("OPTION")
                    opt.add_column("Discription")
                    opt.add_row(
                        "ALL", "set debuggable & networkSecurityConfig, build & sign APK ")
                    opt.add_row(
                        "DEBUGABLE", "set debuggable, build & sign APK")
                    opt.add_row(
                        "NETWORK", "set networkSecurityConfig, build & sign APK")
                    opt.add_row("INFO", "identify the package name")
                    opt.add_row(
                        "SCREENSHOT", "get screenshot from connected device")
                    opt.add_row("DECODE", "decode APK")
                    opt.add_row("BUILD", "build APK")
                    opt.add_row("SIGN", "sign APK")
                    opt.add_row("ALIGN", "align")
                    console.print(opt)
                case 'return':
                    main()
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")


def main():
    command = ""
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
                    table.add_row("2", "apkutil")
                    table.add_row("3", "andropass")
                    console.print(table)
                case 'START install_tools':
                    installer()
                case 'START apkleaks':
                    apkleaks(fn)
                case 'START apkutil':
                    apkutil(fn)
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
                    hm.add_row("START apkutil", "Use APKUtil tool")
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
