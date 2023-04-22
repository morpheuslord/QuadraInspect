import os
import platform
from subprocess import run
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from subprocess import run
console = Console()

def apkleaks(fn, rdir):
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
                        b=tdir, c=final_cmd, d=tfile), shell=True)
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
                    opt.add_row("return", "return to main menu")
                    opt.add_row("quit", "quit the program")
                    console.print(opt)
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")
