import os
import platform
from subprocess import run
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from subprocess import run
console = Console()


def backdoor(fn, rdir):
    outputloc = '{a}/results/'.format(a=rdir)
    os.mkdir('{a}/{b}'.format(a=outputloc, b=fn))
    outdir = ('{a}/{b}'.format(a=outputloc, b=fn))
    try:
        osp = platform.system()
        p = ""
        match osp:
            case 'Darwin':
                p = "sudo bash "
            case 'Linux':
                p = "sudo bash "
        rdir = os.getcwd()
        tdir = '{}/tools/backdoor-apk-master/backdoor-apk'.format(rdir)
        tfile = '{x}/target/{y}'.format(x=rdir, y=fn)
        while True:
            command = Prompt.ask("backdoor>> ")
            match command:
                case 'attack':
                    run("{a} {b}backdoor-apk.sh {c}".format(
                        a=p, b=tdir, c=tfile), shell=True)
                    try:
                        run("cp -r out {}".format(outdir))
                    except:
                        pass
                    try:
                        run("cp backdoor-apk.rc {}".format(outdir))
                    except:
                        pass
                case 'quit':
                    quit()

                case 'SHOW OPTIONS':
                    opt = Table(title="Options SET")
                    opt.add_column("OPTION")
                    opt.add_column("SET Value")
                    opt.add_row("TARGET", str(fn))
                    opt.add_row("OUTPUT", str(outdir))
                    console.print(opt)
                    pprint(
                        "Use any one mode at once more than one mode wont work and my cause errors")
                case 'quit':
                    quit()
    except KeyboardInterrupt:
        pprint("Ending process ...")
