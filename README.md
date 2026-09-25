# QuadraInspect

```
   ____                  __           ____                           __ 
  / /\ \__  ______ _____/ /________ _/  _/___  _________  ___  _____/ /_
 / / / / / / / __ `/ __  / ___/ __ `// // __ \/ ___/ __ \/ _ \/ ___/ __/
/ /_/ / /_/ / /_/ / /_/ / /  / /_/ // // / / (__  ) /_/ /  __/ /__/ /_  
\___\\_\__,_/\__,_/\__,_/_/   \__,_/___/_/ /_/____/ .___/\___/\___/\__/  
                                                /_/                     
```
<p align="center">
         <img src="https://img.shields.io/badge/Os-Linux-yellow?logo=linux" />
         <img src="https://img.shields.io/badge/Os-windows-yellow?logo=windows" />
         <img src="https://img.shields.io/badge/Os-mac-yellow?logo=macos" />
</p>
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

QuadraInspect is packaged as a standard Python project and is managed with the
[`uv`](https://docs.astral.sh/uv/) package manager.

## Installation

### Quick install (everything at once)

The fastest path — installs `uv`, all Python dependencies, **and** every
integrated tool and add-on in a single command:

```bash
git clone https://github.com/morpheuslord/QuadraInspect
cd QuadraInspect
./install.sh            # Linux / macOS  (use sudo where tools require it)
```

On Windows, run `install.bat` from the cloned directory. Pass `--deps-only` to
install just the Python dependencies and skip the tools.

The step-by-step instructions below do the same thing manually.

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

(See the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
for Windows and alternative methods.)

### 2. Clone and set up the framework

```bash
git clone https://github.com/morpheuslord/QuadraInspect
cd QuadraInspect
uv sync
```

`uv sync` creates an isolated virtual environment and installs QuadraInspect from
the locked dependency set (`uv.lock`). The bundled analysis scripts pull a few
extra libraries; install them with:

```bash
uv sync --extra tools
```

### 3. Run QuadraInspect

```bash
uv run quadrainspect            # interactive (frame) mode
```

You can also run it as a module or via the legacy entry point:

```bash
uv run python -m quadrainspect
uv run python main.py
```

> On Linux/macOS some integrated tools require elevated privileges; run the
> command with `sudo` where needed.

### 4. Install the integrated tools

Once QuadraInspect loads, run:

```
QuadraInspect Main>> START install_tools
```

To install the integrated tools **and** every optional add-on in one step, use:

```
QuadraInspect Main>> START full_install
```

The tools are downloaded to the `tools` directory and each tool's own setup steps
run automatically.

## Addins

Add-ins are optional, community-contributed tools. They are declared as `AddOn`
objects in `quadrainspect/tools/addins.py`, so contributing a new one is a matter
of adding a single entry with its dependencies and an install callable — no
`switch`/`match` statement to edit.

- The framework (and its add-ins) can be updated using the `update addins` or the
  `update-addins` commands, which perform a `git pull` on the checkout.
- As of now the available add-ins are **APKEditor** and **Backdoor-APK**. Install
  them with the `START addins` command; both require a Java runtime environment.

## Usage
Each module has a help function so that the commands and the descriptions are detailed and can be altered for operation.

### OS and modes
- In linux and Mac you need to run it as a `sudo` user
- In Windows only the installation can be done as a `Admin` rest all can be done as a normal user 

These are the key points that must be addressed for smooth working:
- The APK file or target must be declared before starting any attack 
- The Attacks are separate entities combined via this framework doing research on how to use them is recommended.
- The APK file can be either declared either using `args` or using `SET target` withing the tool.
- The target APK file must be placed in the `target` folder as all the tool searches for the target file with that folder.

### Modes
There are 2 modes:
```
|
└─> F mode
└─> A mode
```
#### F mode
The `f` mode is a mode where you get the active interface for using the interactive variation of the framework with the prompt, etc.

![Usage](https://user-images.githubusercontent.com/70637311/230757399-e5a4fea3-8932-4ddb-9dfa-99ee35d7994d.png)

F mode is the normal mode and can be used easily

#### A mode
A mode or argumentative mode takes the input via arguments and runs the commands without any intervention by the user this is limited to the main menu in the future i am planning to extend this feature to even the incorporated codes.

```bash
uv run quadrainspect --target <APK_file> --mode argm --command install_tools/tools_name/apkleaks/mobfs/rms/apkleaks
```
![Argument_mode](https://user-images.githubusercontent.com/70637311/230757449-a690fe49-ee22-4f78-bc62-0ca33eeec2da.png)

### Main Module
the main menu of the entire tool has these options and commands:

`Frame mode`:
|Command|Description|
|----|----|
|`SET target`| SET the name of the targetfile|
|`START install_tools`|If not installed this will install the tools|
|`START full_install`| Install all tools and add-ons at once |
|`LIST tools_name`| List out the Tools Integrated |
|`START apkleaks`|  Use APKLeaks tool |
|`START mobfs`| Use MOBfs for dynamic and static analysis |
|`START andropass`| Use AndroPass APK analizer |
|`START addins` | Starts the Extra tools installer |
|`update addins`| Updates the extra tools installer|
|`help`| Display help menu|
|`SHOW banner`| Display banner|
|`quit`|Quit the program|

`Args mode`:
|Command|Description|
|----|----|
|`install_tools`|If not installed this will install the tools|
|`full-install`| Install all tools and add-ons at once |
|`tools_name`| List out the Tools Integrated |
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
Mobfs is pretty straight forward only the port number must be taken care of which is by default on port 5000 you just need to start the program and connect to it on `127.0.0.1:5000` over your browser.

### AndroPass
AndroPass is also really straight forward it just takes the file as input and does its job without any other inputs.

## Architecture

QuadraInspect follows a modular, object-oriented architecture. The framework core
lives in the `quadrainspect` package and each integrated tool is a self-contained
class.

```
quadrainspect/
├── cli.py          # argument parsing / process entry point
├── app.py          # orchestrator + shared frame/argument menu spec
├── shell.py        # interactive REPL base class
├── registry.py     # command registry (dispatch + auto-generated help)
├── runner.py       # centralised subprocess execution (no shell injection)
├── platform.py     # OS abstraction
├── session.py      # workspace layout + runtime state (target, paths)
├── console.py      # shared console, logging, banner
├── net.py          # dependency-free downloads
├── exceptions.py   # typed error hierarchy
└── tools/          # one class per integrated tool
    ├── base.py         # Tool / OneShotTool / InteractiveTool + ToolContext
    ├── apkleaks.py, apkeditor.py, andropass.py, backdoor.py,
    ├── mobfs.py, rms.py, installer.py, addins.py, updater.py
```

Key design points:

- **Command registry (arbitration):** user input is dispatched through a
  `CommandRegistry` of first-class `Command` objects instead of large duplicated
  `match`/`switch` blocks. Help tables are generated from the same registry, so
  they can never drift out of sync with the commands.
- **Single menu source of truth:** frame (interactive) and argument modes are both
  driven by one list of `MenuEntry` objects in `app.py`.
- **Safe subprocess handling:** every external command runs through
  `CommandRunner` as an argument list (`shell=False`), so user-supplied values
  such as target file names can never be interpreted by a shell.
- **Typed errors:** operational failures raise subclasses of
  `QuadraInspectError` and are reported cleanly by the REPL instead of crashing it.

### Adding a new tool

1. Create a class in `quadrainspect/tools/` extending `OneShotTool` (single
   action) or `InteractiveTool` (its own sub-menu). Use `self.runner`,
   `self.session` and `self.platform` from the shared `ToolContext`.
2. Export it from `quadrainspect/tools/__init__.py`.
3. Add one `MenuEntry` for it in `QuadraInspect._build_menu` (`app.py`). That
   single entry registers the tool in **both** frame and argument modes and in the
   help output.
4. If the tool needs to be downloaded, add its repository to `Installer`.

If wanted you could do your upgrades and add them to this repository for more
people to use, growing this tool.

### Docker 
Still under development

## Contributions

Anyone can contribute. I want this tool to be useful for as many people as possible. If anyone wants to contribute please feel free to. One way you can contribute is by adding your tools or tools you feel like can add value to the code and the complete framework.
