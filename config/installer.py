import os
import platform
from git import Repo
from subprocess import run
from rich.console import Console
from rich.pretty import pprint

console = Console()
os.chdir(os.getcwd())
path = str(os.getcwd())
fn = ""

def installer(rdir):
    pprint("Validating OS:")
    osp = platform.system()
    pprint("OS FOUND: {}".format(osp))
    command = ""
    cmd_mob = ""
    match osp:
        case 'Darwin':
            command = "python3 setup.py build && python3 setup.py install"
            cmd_mob = "sudo bash setup.sh"
        case 'Linux':
            command = "python3 setup.py build && python3 setup.py install"
            cmd_mob = "sudo bash setup.sh"
        case 'Windows':
            command = "python setup.py build && python setup.py install"
            cmd_mob = ".\setup.bat"
    andropass = 'https://github.com/koengu/AndRoPass'
    apkleaks = 'https://github.com/dwisiswant0/apkleaks'
    mobfs = 'https://github.com/MobSF/Mobile-Security-Framework-MobSF.git'
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
    pprint('This may take some time be patient...')
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
    pprint("Cloning MOBfs")
    try:
        Repo.clone_from(mobfs, '{}/mobfs'.format(twd))
    except:
        pass
    os.chdir('{}/apkleaks'.format(twd))
    run(command, shell=True)
    os.chdir('{}/mobfs'.format(twd))
    run(cmd_mob, shell=True)
    pprint('Install Complete')
