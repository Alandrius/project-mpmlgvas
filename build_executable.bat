@echo off
setlocal

echo Starting Windows build...

REM Move to project root (folder with this .bat)
cd /d "%~dp0"

REM Choose Python launcher
where py >nul 2>nul
if %errorlevel%==0 (
    set PY_CMD=py -3
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PY_CMD=python
    ) else (
        echo Error: Python is not installed or not in PATH.
        pause
        exit /b 1
    )
)

echo Using: %PY_CMD%

echo Installing PyInstaller...
%PY_CMD% -m pip install pyinstaller
if errorlevel 1 (
    echo Failed to install PyInstaller.
    pause
    exit /b 1
)

echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist assistant.spec del /q assistant.spec

echo Building .exe...
%PY_CMD% -m PyInstaller --onefile --name assistant assistant.py
if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)

echo Done.
echo Executable: dist\assistant.exe
pause
