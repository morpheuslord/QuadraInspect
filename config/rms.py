import os
from rich.pretty import pprint
from subprocess import run


def rms(rdir):
    try:
        tdir = '{}/tools/rms/'.format(rdir)
        os.chdir(tdir)
        run('node rms.js 127.0.0.1:5000')
        pass
    except KeyboardInterrupt:
        pprint("Ending process ...")
