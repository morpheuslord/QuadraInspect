@echo off
REM Complete installer for QuadraInspect (Windows).
REM
REM One command to go from a fresh clone to a fully working setup:
REM   1. install uv (if missing)
REM   2. install all Python dependencies (core + analysis-script extras)
REM   3. download and set up every integrated tool and add-on
REM
REM Usage:
REM   install.bat            dependencies + tools + add-ons
REM   install.bat --deps-only    only the Python dependencies

setlocal
cd /d "%~dp0"

where uv >nul 2>&1
if errorlevel 1 (
    echo [*] Installing uv package manager...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

echo [*] Installing Python dependencies...
uv sync --extra tools
if errorlevel 1 exit /b 1

if "%~1"=="--deps-only" (
    echo [*] Dependencies installed. Skipping tools ^(--deps-only^).
    exit /b 0
)

echo [*] Installing integrated tools and add-ons...
uv run quadrainspect --mode argm --command full-install

echo [*] Complete installation finished.
echo [*] Run "uv run quadrainspect" to start.
endlocal
