import os
from git import Repo
from subprocess import run
from subprocess import check_output, STDOUT
from rich.pretty import pprint
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from subprocess import run
console = Console()


def addmenu():
    table = Table(title="Tools Menu")
    table.add_column("Number")
    table.add_column("Name")
    table.add_column("OS")
    table.add_column("Depends/Program")
    table.add_row("1", "APKeditor", "Windows/Linux/Unix", "Java")
    console.print(table)


def addinstall(rdir, opt):
    try:
        os.chdir("{}/tools".format(rdir))
        cwd = os.getcwd()
        match opt:
            # SWITCH CASE FOR EACH TOOL
            case '1':
                try:
                    try:
                        # CHECK TO ENSURE THE NECESSARY PROGRAMS ARE PRESENT (IF NECESSARY)
                        print(check_output("java -version",
                                           stderr=STDOUT, shell=True).decode('utf-8'))
                    except OSError:
                        print("java not found on path")
                        quit
                    pprint('Installing APKeditor')
                    # FILE OR REPO LINK
                    link = "https://github.com/REAndroid/APKEditor/releases/download/V1.1.8/APKEditor-1.1.8.jar"
                    # CONFIG FILE LOCATION
                    link2 = "https://raw.githubusercontent.com/morpheuslord/QuadraInspect/main/config/apkeditor.py"
                    # PRE DOWNLOAD PREP
                    os.mkdir('{}/apkeditor'.format(cwd))
                    os.chdir('{}/apkeditor'.format(cwd))
                    # TOOL DOWNLOAD
                    run('wget {} -O apkeditor.jar'.format(link), shell=True)
                    # MOVE TO CONFIGS
                    os.chdir('{}/config'.format(rdir))
                    # CONFIG DOWNLOAD
                    run('wget {} -O apkeditor.py'.format(link2), shell=True)
                except FileNotFoundError:
                    pprint('APKEDITOR file error')
                except:
                    pprint('EXTERNAL errors')

    except FileNotFoundError:
        pprint('Not Able to Change DIR')

# USE THIS FUNCTION INCASE ANY REQUIREMENTS ARE NOT MET AND MUST BE DOWNLOADED
def requirements(opt):
    pass


def addins(rdir):
    while True:
        cmd = Prompt.ask("Addins Main>> ")
        match cmd:
            case 'help':
                addmenu()
            case 'quit':
                quit()
            case 'install':
                opt = Prompt.ask("Addins Main>> ")
                addinstall(rdir, opt)
