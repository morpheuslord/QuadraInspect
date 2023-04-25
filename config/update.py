import os
import platform
from subprocess import run
from rich.pretty import pprint


def update_addins(rdir):
    ifile = "{}/config/additional.py".format(rdir)
    cdir = "{}/config/".format(rdir)
    try:
        osp = platform.system()
        p = ""
        match osp:
            case 'Darwin':
                p = "sudo rm -rf"
            case 'Linux':
                p = "sudo rm -rf"
            case 'Windows':
                p = "del"
        pprint = "Deleting old installer"
        run('{a} {b}'.format(a=p, b=ifile))
        pprint = "Dowloading new installer"
        os.chdir(cdir)
        run('wget https://raw.githubusercontent.com/morpheuslord/QuadraInspect/main/config/additional.py -O additional.py')
    except:
        pprint("Error while deletion or copy")
