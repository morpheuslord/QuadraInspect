# QuadraInspect

```
   ____                  __           ____                           __ 
  / __ \__  ______ _____/ /________ _/  _/___  _________  ___  _____/ /_
 / / / / / / / __ `/ __  / ___/ __ `// // __ \/ ___/ __ \/ _ \/ ___/ __/
/ /_/ / /_/ / /_/ / /_/ / /  / /_/ // // / / (__  ) /_/ /  __/ /__/ /_  
\___\_\__,_/\__,_/\__,_/_/   \__,_/___/_/ /_/____/ .___/\___/\___/\__/  
                                                /_/                     
```
<p align="center">
         <img src="https://img.shields.io/badge/Os-Linux-yellow?logo=linux" />
         <img src="https://img.shields.io/badge/Os-windows-yellow?logo=windows" />
         <img src="https://img.shields.io/badge/Os-mac-yellow?logo=macos" />
</p>
<p align="center">
The security of mobile devices has become a critical concern due to the increasing amount of sensitive data being stored on them. With the rise of Android OS as the most popular mobile platform, the need for effective tools to assess its security has also increased. In response to this need, a new Android framework has emerged that combines three powerful tools - AndroPass, APKUtil, RMS, and MobFS - to conduct comprehensive vulnerability analysis of Android applications. This framework is known as QuadraInspect.

QuadraInspect is an Android framework that integrates AndroPass, APKUtil, RMS and MobFS, providing a powerful tool for analyzing the security of Android applications. AndroPass is a tool that focuses on analyzing the security of Android applications' authentication and authorization mechanisms, while APKUtil is a tool that extracts valuable information from an APK file. Lastly, MobFS and RMS facilitates the analysis of an application's filesystem by mounting its storage in a virtual environment.

By combining these three tools, QuadraInspect provides a comprehensive approach to vulnerability analysis of Android applications. This framework can be used by developers, security researchers, and penetration testers to assess the security of their own or third-party applications. QuadraInspect provides a unified interface for all three tools, making it easier to use and reducing the time required to conduct comprehensive vulnerability analysis. Ultimately, this framework aims to increase the security of Android applications and protect users' sensitive data from potential threats.

## Requirements
 - Windows, Linux or Mac
 - NodeJs installed
 - Python 3.10 or above installed
 - OpenSSL-3 installed
 - Wkhtmltopdf installed
 - Additional things based on the addins

## Installation

### Install python3.10 on ubuntu or other linux
- Step 0: prerequisite
```bash
sudo apt install wget build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev  
```
- Step 1: download python
```bash
sudo su && wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz && tar xzf Python-3.10.8.tgz && cd Python-3.10.8 
```
- Step 2: install python
```bash
./configure --enable-optimizations 
make altinstall 
```
### Install the tool

To install the tools you need to:
First : 
`
git clone https://github.com/morpheuslord/QuadraInspect
`

Second Open a **Administrative** cmd or powershell (for Mobfs setup) and run : 
```bash
pip install -r requirements.txt && python main.py
``` 

or

```bash
sudo pip3.10 install -r requirements.txt && sudo python3.10 main.py
```

Third : Once QuadraInspect loads run this command
`
QuadraInspect Main>> : START install_tools
`

The tools will be downloaded to the `tools` directory and also the setup.py and setup.bat commands will run automatically for the complete installation.

## Addins

The addins are for the community to edit. Anyone who is intrested can add new tools by editing the `config/additional.py` file and the tools and all the perticular configurations necessary for the smooth installation of the program.

- The addins can be updated using the `update addins` or the `update-addins` commands depending on the mode of usage.
- For each Addin a currsponding config file must be written and placed in the `config` directory.
- Each of the tools must be updating the `main.py` also.
Hope many more tools will be added by you all as a support and building of the tool.

As of now there is one additional tool called APKEditor mentioned in the addins. You can install that from the `START addins` command and needs `java RTE` to run

## Usage
Each module has a help function so that the commands and the discriptions are detailed and can be altered for operation.

### OS and modes
- In linux and Mac you need to run it as a `sudo` user
- In Windows only the installation can be done as a `Admin` rest all can be done as a normal user 

These are the key points that must be addressed for smooth working:
- The APK file or target must be declared before starting any attack 
- The Attacks are seperate entities combined via this framework doing research on how to use them is recommended.
- The APK file can be ether declared ether using `args` or using `SET target` withing the tool.
- The target APK file must be placed in the `target` folder as all the tool searches for the target file with that folder.

### Modes
There are 2 modes:
```
|
└─> F mode
└─> A mode
```
#### F mode
The `f` mode is a mode where you get the active interface for using the interactive vaerion of the framework with the prompt, etc.

![Usage](https://user-images.githubusercontent.com/70637311/230757399-e5a4fea3-8932-4ddb-9dfa-99ee35d7994d.png)

F mode is the normal mode and can be used easily

#### A mode
A mode or argumentative mode takes the input via arguments and runs the commands without any intervention by the user this is limited to the main menu in the future i am planning to extend this feature to even the encorporated codes.

```bash
python main.py --target <APK_file> --mode a --command install_tools/tools_name/apkleaks/mobfs/rms/apkleaks
```
![Argument_mode](https://user-images.githubusercontent.com/70637311/230757449-a690fe49-ee22-4f78-bc62-0ca33eeec2da.png)

### Main Module
the main menu of the entire tool has these options and commands:

`Frame mode`:
|Command|Discription|
|----|----|
|`SET target`| SET the name of the targetfile|
|`START install_tools`|If not installed this will install the tools|
|`LIST tools_name`| List out the Tools Intigrated |
|`START apkleaks`|  Use APKLeaks tool |
|`START mobfs`| Use MOBfs for dynamic and static analysis |
|`START andropass`| Use AndroPass APK analizer |
|`START addins` | Starts the Extra tools installer |
|`update addins`| Updates the extra tools installer|
|`help`| Display help menu|
|`SHOW banner`| Display banner|
|`quit`|Quit the program|

`Args mode`:
|Command|Discription|
|----|----|
|`install_tools`|If not installed this will install the tools|
|`tools_name`| List out the Tools Intigrated |
|`apkleaks`|  Use APKLeaks tool |
|`mobfs`| Use MOBfs for dynamic and static analysis |
|`andropass`| Use AndroPass APK analizer |
|`addins` | Starts the Extra tools installer |
|`addins`| Updates the extra tools installer|
|`help`| Display help menu|
|`banner`| Display banner|

As mentioned above the target must be set before any tool is used.

### Apkleaks menu
The APKLeaks menu is also really straight forward and only a few things to consider:
- The options `SET output` and `SET json-out` takes file names not the actual files it creates an output in the `result` directory.
- The `SET pattern` option takes a name of a json pattern file. The JSON file must be located in the `pattern` directory

| OPTION      | SET Value |
|-------------|-----------|
|`SET output` |Output for the scan data file name|
|`SET arguments`   | Additional Disassembly arguments|
|`SET json-out` | JSON output file name|
|`SET pattern `    | The pre-searching pattern for secrets|
|`help`|Displays help menu|
|`return` |Return to main menu|
|`quit`|Quit the tool|

### Mobfs
Mobfs is pritty straight forward only the port number must be taken care of which is by default on port 5000 you just need to start the program and connect to it on `127.0.0.1:5000` over your browser.

### AndroPass
AndroPass is also really straight forward it just takes the file as input and does its job without any other inputs.

## Architecture:

The APK analysis framework will follow a modular architecture, similar to Metasploit. It will consist of the following modules:

- Core module: The core module will provide the basic functionality of the framework, such as command-line interface, input/output handling, and logging.
- Static analysis module: The static analysis module will be responsible for analyzing the structure and content of APK files, such as the manifest file, resources, and code.
- Dynamic analysis module: The dynamic analysis module will be responsible for analyzing the behavior of APK files, such as network traffic, API calls, and file system interactions.
- Reverse engineering module: The reverse engineering module will be responsible for decompiling and analyzing the source code of APK files.
- Vulnerability testing module: The vulnerability testing module will be responsible for testing the security of APK files, such as identifying vulnerabilities and exploits.

### Adding more

Currentluy there only 3 but if wanted people can add more tools to this these are the things to be considered:
- Installer function
- Seperate tool function
- Main function

#### Installer Function

- Must edit in the `config/installer.py`
- The things to consider in the installer is the link for the repository.
- keep the cloner and the directory in a try-except condition to avoide errors.
- choose an appropriate command for further installation

#### Seperate tool function

- Must edit in the `config/mobfs.py , config/androp.py, config/apkleaks.py`
- Write a new function for the specific tool
- File handeling is up to you I recommend passing the file name as an argument and then using the name to locate the file using the subprocess function
- the tools must also recommended to be in a try-except condition to avoide unwanted errors.

#### Main Function
- A new case must be added to the switch function to act as a main function holder
- the help menu listing and commands are up to your requirements and comfort

If wanted you could do your upgrades and add it to this repository for more people to use kind of growing this tool.

### Docker 
Still under development

## Contributions

Anyone can contribute. I want this tool to be useful for as many people as possible. If anyone wants to contribute please feel free to. One way you can contribute is by adding your tools or tools you feel like can add value to the code and the complete framework.
