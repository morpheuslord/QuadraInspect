import os
import platform
from subprocess import run
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from subprocess import run
console = Console()


def apkeditor(fn, rdir):
    DECOMP = ""
    BUILD = ""
    MERGE = ""
    REFACTOR = ""
    PROTECT = ""
    outputloc = '{a}/results/{b}'.format(a=rdir, b=fn)
    try:
        osp = platform.system()
        p = ""
        match osp:
            case 'Darwin':
                p = "java -jar"
            case 'Linux':
                p = "java -jar"
            case 'Windows':
                p = "java -jar"
        rdir = os.getcwd()
        tdir = '{}/tools/apkeditor/'.format(rdir)
        tfile = '{x}/target/{y}'.format(x=rdir, y=fn)
        final_cmd = str("")
        while True:
            command = Prompt.ask("APKEDTOR>> ")
            match command:
                case 'SET decode':
                    DECOMP = "TRUE"
                    final_cmd += str(" d -i {a} -o {b}{c}".format(a=tfile,
                                     b=outputloc, c=fn))

                case 'SET merge':
                    MERGE = "TRUE"
                    TLOC = Prompt.ask("TARGET DIR LOC>> ")
                    os.chdir(outputloc)
                    final_cmd += str(" m -i {} ".format(TLOC))
                    os.chdir(rdir)

                case 'SET build':
                    BUILD = "TRUE"
                    TLOC = Prompt.ask("TARGET DIR LOC>> ")
                    os.chdir(outputloc)
                    final_cmd += str(" b -i {} ".format(TLOC))
                    os.chdir(rdir)

                case 'SET refactor':
                    REFACTOR = "TRUE"
                    final_cmd += str(" x -i {a} -o {b}{c}".format(a=tfile,
                                     b=outputloc, c=fn))

                case 'SET protect':
                    PROTECT = "TRUE"
                    final_cmd += str(" p -i {a} -o {b}{c}".format(a=tfile,
                                     b=outputloc, c=fn))

                case 'attack':
                    run("{a} {b}apkeditor.jar {c}".format(
                        a=p, b=tdir, c=final_cmd), shell=True)

                case 'quit':
                    quit()

                case 'SHOW OPTIONS':
                    opt = Table(title="Options SET")
                    opt.add_column("OPTION")
                    opt.add_column("SET Value")
                    opt.add_row("TARGET", str(fn))
                    opt.add_row("OUTPUT", str(outputloc))
                    opt.add_row("DECODE", str(DECOMP))
                    opt.add_row("MERGE", str(BUILD))
                    opt.add_row("REFCTOR", str(MERGE))
                    opt.add_row("BUILD", str(REFACTOR))
                    opt.add_row("PROTECT", str(PROTECT))
                    console.print(opt)
                case 'help':
                    opt = Table(title="APKLeaks Help Menu")
                    opt.add_column("OPTION")
                    opt.add_column("Discription")
                    opt.add_row("SET decode",
                                "Decompiles APK file")
                    opt.add_row("SET merge", "Merges 2 or more APK files")
                    opt.add_row(
                        "SET build", "Builds APK from decompiled files")
                    opt.add_row("SET refactor",
                                "Refactors obfuscated APK file")
                    opt.add_row("SET protect",
                                "Safeguard APK file from decompilers")
                    opt.add_row("SHOW OPTIONS", "DISPLAY enabled options")
                    opt.add_row("help", "Displays help menu")
                    opt.add_row("quit", "quit the program")
                    console.print(opt)
                    pprint(
                        "Use any one mode at once more than one mode wont work and my cause errors")
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")
