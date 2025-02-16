@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing now...
    winget install -e --id Python.Python.3 -h
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install Python. Please check winget setup.
        pause
        exit /b
    )
)

:: Verify Python installation
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Python installation verification failed. Exiting...
    pause
    exit /b
)

:: Install required libraries
echo Installing required Python libraries...
python -m pip install --upgrade pip
python -m pip install faker selenium plyer psutil pyautogui
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install Python libraries. Exiting...
    pause
    exit /b
)

:: Define the path to the desktop
set "desktop_path=%USERPROFILE%\Desktop"

:: Download and extract Geckodriver
echo Downloading Geckodriver...
if not exist "%desktop_path%\geckodriver" (
    echo Downloading Geckodriver zip and extracting...
    curl -L https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.35.0-win64.zip -o "%desktop_path%\geckodriver.zip" && powershell -Command "Expand-Archive -Path '%desktop_path%\geckodriver.zip' -DestinationPath '%desktop_path%'"
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to download or extract Geckodriver. Exiting...
        pause
        exit /b
    )
    echo Geckodriver extracted successfully.
) else (
    echo Geckodriver already exists on the desktop.
)

:: Run the Python script
echo Running the Python script...
python newcode.py
if %ERRORLEVEL% NEQ 0 (
    echo The script encountered an error. Exiting...
    pause
    exit /b
)

pause
