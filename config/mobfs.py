from rich.pretty import pprint
from subprocess import run

def mobfs(rdir):
    try:
        tdir = '{}/tools/mobfs/'.format(rdir)
        run('{}/run.bat 127.0.0.1:5000'.format(tdir))
        pass
    except KeyboardInterrupt:
        pprint("Ending process ...")