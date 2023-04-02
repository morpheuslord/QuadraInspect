# AFrame

The security of mobile devices has become a critical concern due to the increasing amount of sensitive data being stored on them. With the rise of Android OS as the most popular mobile platform, the need for effective tools to assess its security has also increased. In response to this need, a new Android framework has emerged that combines three powerful tools - AndroPass, APKUtil, and MobFS - to conduct comprehensive vulnerability analysis of Android applications.

AndroPass is a tool that focuses on analyzing the security of Android applications' authentication and authorization mechanisms. It can perform a detailed analysis of an application's source code, identifying any potential weaknesses in the app's authentication and authorization protocols. APKUtil, on the other hand, is a tool that extracts valuable information from an APK file, including the application's manifest, resources, and source code. It can be used to analyze an app's behavior, including its network activity and the permissions it requests.

Lastly, MobFS is a tool that facilitates the analysis of an application's filesystem by mounting its storage in a virtual environment. This tool can be particularly useful when examining sensitive data stored by an application, such as login credentials or personal information.

By combining these three tools, the Android framework provides a comprehensive approach to vulnerability analysis of Android applications. This framework can be used by developers, security researchers, and penetration testers to assess the security of their own or third-party applications. Ultimately, this framework aims to increase the security of Android applications and protect users' sensitive data from potential threats.

## Installation

To install the tools you need to:
First : 
`
git clone https://github.com/morpheuslord/AFrame
`

Second Open a **Administrative** cmd or powershell (for Mobfs setup) and run : 
`
pip install -r requirements.txt && pytbon3 main.py
`

Third : Once AFrame loads run this command
`
AFrame Main>> : START install_tools
`

The tools will be downloaded to the `tools` directory and also the setup.py and setup.bat commands will run automatically for the complete installation.

## Usage
Each module has a help function so that the commands and the discriptions are detailed and can be altered for operation.

These are the key points that must be addressed for smooth working:
- The APK file or target must be declared before starting any attack 
- The Attacks are seperate entities combined via this framework doing research on how to use them is recommended.
- The APK file can be ether declared ether using `args` or using `SET target` withing the tool.
- The target APK file must be placed in the `target` folder as all the tool searches for the target file with that folder.

### Main Module

## Architecture:

The APK analysis framework will follow a modular architecture, similar to Metasploit. It will consist of the following modules:

- Core module: The core module will provide the basic functionality of the framework, such as command-line interface, input/output handling, and logging.
- Static analysis module: The static analysis module will be responsible for analyzing the structure and content of APK files, such as the manifest file, resources, and code.
- Dynamic analysis module: The dynamic analysis module will be responsible for analyzing the behavior of APK files, such as network traffic, API calls, and file system interactions.
- Reverse engineering module: The reverse engineering module will be responsible for decompiling and analyzing the source code of APK files.
- Vulnerability testing module: The vulnerability testing module will be responsible for testing the security of APK files, such as identifying vulnerabilities and exploits.
