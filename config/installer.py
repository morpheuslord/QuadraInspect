import os
import platform
from git import Repo
from subprocess import run
from git.remote import RemoteProgress
from rich.console import Console
from rich.pretty import pprint
from rich.progress import track

console = Console()
os.chdir(os.getcwd())
path = str(os.getcwd())
fn = ""


class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        pprint('update(%s, %s, %s, %s)' %
              (op_code, cur_count, max_count, message))


def installer(rdir):
    pprint("Validating OS:")
    osp = platform.system()
    pprint("OS FOUND: {}".format(osp))
    command = ""
    cmd_mob = ""
    rms_cmd = ""
    match osp:
        case 'Darwin':
            command = "python3 setup.py build && python3 setup.py install"
            cmd_mob = "sudo bash setup.sh"
            rms_cmd = "npm install -g rms-runtime-mobile-security"
        case 'Linux':
            command = "python3 setup.py build && python3 setup.py install"
            cmd_mob = "sudo bash setup.sh"
            rms_cmd = "npm install -g rms-runtime-mobile-security"
        case 'Windows':
            command = "python setup.py build && python setup.py install"
            cmd_mob = ".\setup.bat"
            rms_cmd = "npm install -g rms-runtime-mobile-security"
    andropass = 'https://github.com/koengu/AndRoPass'
    apkleaks = 'https://github.com/dwisiswant0/apkleaks'
    mobfs = 'https://github.com/MobSF/Mobile-Security-Framework-MobSF.git'
    rms = 'https://github.com/m0bilesecurity/RMS-Runtime-Mobile-Security'
    os.chdir(rdir)
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
        Repo.clone_from(andropass, '{}/andropass'.format(twd),
                        progress=Progress())
    except:
        pass
    pprint("Cloning APKLeaks")
    try:
        Repo.clone_from(apkleaks, '{}/apkleaks'.format(twd),
                        progress=Progress())
    except:
        pass
    pprint("Cloning MOBfs")
    try:
        Repo.clone_from(mobfs, '{}/mobfs'.format(twd), progress=Progress())
    except:
        pass
    pprint("Cloning RMS-Mobile-Security")
    try:
        Repo.clone_from(rms, '{}/rms'.format(twd), progress=Progress())
    except:
        pass
    os.chdir('{}/apkleaks'.format(twd))
    run(command, shell=True)
    os.chdir('{}/mobfs'.format(twd))
    run(cmd_mob, shell=True)
    os.chdir('{}/rms'.format(twd))
    run(rms_cmd, shell=True)
    run('npm install express nunjucks')
    pprint('Install Complete')
