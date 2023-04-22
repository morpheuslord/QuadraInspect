import os
import platform
from subprocess import run
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from subprocess import run
console = Console()

def androp(fn, rdir):
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
                    run("{a} {b}AndRoPass.py -a {c}".format(a=p, b=tdir, c=tfile), shell=True)
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
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")
