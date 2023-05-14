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
    table.add_row("2", "Backdoor-Apk-Master",
                  "Linux/Unix (Tested Kali Linux)", "Java")
    console.print(table)


def addinstall(rdir, opt):
    try:
        os.chdir("{}/tools".format(rdir))
        cwd = ("{}/tools".format(rdir))
        match opt:
            case '1':
                try:
                    try:
                        print(check_output("java -version",
                                           stderr=STDOUT, shell=True).decode('utf-8'))
                    except OSError:
                        print("java not found on path")
                        quit
                    pprint('Installing APKeditor')
                    link = "https://github.com/REAndroid/APKEditor/releases/download/V1.1.8/APKEditor-1.1.8.jar"
                    link2 = "https://raw.githubusercontent.com/morpheuslord/QuadraInspect/main/config/apkeditor.py"
                    try:
                        os.mkdir('{}/apkeditor'.format(cwd))
                    except:
                        pass
                    os.chdir('{}/apkeditor'.format(cwd))
                    run('wget {} -O apkeditor.jar'.format(link), shell=True)
                    os.chdir('{}/config'.format(rdir))
                    # CONFIG DOWNLOAD
                    try:
                        run('wget {} -O apkeditor.py'.format(link2), shell=True)
                    except:
                        pass
                except FileNotFoundError:
                    pprint('APKEDITOR file error')
                except:
                    pprint('EXTERNAL errors')
            case '2':
                try:
                    try:
                        print(check_output("java -version",
                                           stderr=STDOUT, shell=True).decode('utf-8'))
                    except OSError:
                        print("java not found on path")
                        quit
                    try:
                        print(check_output("msfconsole -version",
                                           stderr=STDOUT, shell=True).decode('utf-8'))
                    except OSError:
                        print("metasploit not found on path")
                        pprint("Installing Metasploit")
                        run("curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall &&  chmod 755 msfinstall &&  sudo bash msfinstall", shell=True)
                        quit
                    pprint('Installing Backdoor-Apk-Master')
                    link = "https://github.com/am6539/backdoor-apk-master"
                    link2 = "https://github.com/morpheuslord/QuadraInspect/raw/main/config/backdoor.py"
                    link3 = "https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.5.2.jar"
                    link4 = "https://github.com/iBotPeaches/Apktool/releases/download/v2.7.0/apktool_2.7.0.jar"
                    try:
                        os.mkdir('{}/backdoor-apk-master'.format(cwd))
                    except:
                        pass
                    os.chdir('{}/backdoor-apk-master'.format(cwd))
                    run('git clone {} bak'.format(link), shell=True)
                    d = os.getcwd()
                    tdir = ('{}/backdoor-apk').format(d)
                    run("sudo apt-get update && sudo apt-get upgrade -y", shell=True)
                    run("sudo apt install default-jdk dex2jar unzip proguard zipalign", shell=True)
                    run("wget {} -O baksmali.jar && chmod +x baksmali.jar && mv baksmali.jar baksmali && sudo cp baksmali /bin && sudo cp baksmali /usr/bin".format(link3), shell=True)
                    run("wget {} -O apktool.jar && chmod +x apktool.jar && mv apktool.jar apktool && sudo cp apktool /bin && sudo cp apktool /usr/bin".format(link4), shell=True)
                    run("chmod +x {}/third-party/android-string-obfuscator/lib/aso".format(tdir), shell=True)
                    run("chmod +x {}/third-party/android-string-obfuscator/lib/*".format(tdir), shell=True)
                    run("chmod +x {}/third-party/android-sdk-linux/build-tools/25.0.2/dx".format(tdir), shell=True)
                    run("chmod +x {}/third-party/android-sdk-linux/build-tools/25.0.2/*".format(tdir), shell=True)
                    run("chmod +x {}/third-party/proguard5.3.2/lib/*".format(tdir), shell=True)
                    os.chdir('{}/config'.format(rdir))
                    # CONFIG DOWNLOAD
                    try:
                        run('wget {} -O backdoor.py'.format(link2), shell=True)
                    except:
                        pass
                except FileNotFoundError:
                    pprint('BACKDOOR file error')
                except:
                    pprint('EXTERNAL errors')

    except FileNotFoundError:
        pprint('Not Able to Change DIR')


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
                opt = Prompt.ask("Addins Install option >> ")
                addinstall(rdir, opt)
