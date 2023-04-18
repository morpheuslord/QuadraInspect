import platform
from rich.pretty import pprint
from subprocess import run

def mobfs(rdir):
    osp = platform.system()
    match osp:
        case 'Darwin':
            pre = ""
            cmd = "run.sh"
        case 'Linux':
            pre = ""
            cmd = "run.sh"
        case 'Windows':
            pre = "bash"
            cmd = "run.bat"
    try:
        tdir = '{}/tools/mobfs/'.format(rdir)
        run('{a} {b}/{c}'.format(a=pre, b=tdir, c=cmd))
        pass
    except KeyboardInterrupt:
        pprint("Ending process ...")
