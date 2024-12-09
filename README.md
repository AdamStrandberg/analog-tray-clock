# Analog Tray Clock for Windows

A minimalist analog clock that sits in your Windows system tray. Shows the current time with an elegant design - hours are displayed with a line, and minutes with a dot.

![Clock in light theme](https://raw.githubusercontent.com/adamstrandberg/analog-tray-clock/main/screenshots/light.png)
![Clock in dark theme](https://raw.githubusercontent.com/adamstrandberg/analog-tray-clock/main/screenshots/dark.png)

## Features
- Minimalist analog clock in Windows system tray
- Updates every 10 seconds
- Dark/light theme support
- Clean, modern design

## Usage
1. Download the latest release from the Releases page
2. Run `AnalogTrayClock.exe` from the downloaded folder
3. (Optional) To start automatically with Windows:
   - Press `Win + R`
   - Type `shell:startup`
   - Create a shortcut to `AnalogTrayClock.exe` in the opened folder

## Building
To create a standalone executable:
1. Install PyInstaller: `pip install pyinstaller`
2. Run: `python build.py`

The executable will be created in the `dist` directory.

## Requirements
- Windows 10 or later
- Python 3.6 or later (for development)

## License
MIT