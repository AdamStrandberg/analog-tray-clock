# Analog Tray Clock for Windows

A minimalist analog clock that sits in your Windows system tray. Shows the current time with an elegant design - hours are displayed with a line, and minutes with a dot.

![Screenshot](https://github.com/AdamStrandberg/analog-tray-clock/blob/4df0ffd66f6844d6f17e44f249ffeee0f8f10266/screenshot.png)

⬇️ [Download Analog Tray Clock](https://github.com/AdamStrandberg/analog-tray-clock/releases/download/release-1.1/AnalogTrayClock.exe)

## Features
- Minimalist analog clock in Windows system tray
- Dark/light theme with system detection
- Tiny single-file footprint (~460KB)

## Usage
1. Download the latest release from the Releases page
2. Run `AnalogTrayClock.exe` from the downloaded folder
3. (Optional) To start automatically with Windows:
   - Press `Win + R`
   - Type `shell:startup`
   - Create a shortcut to `AnalogTrayClock.exe` in the opened folder

## Building
```powershell
.\build-single-exe.ps1
```

This script will create a executable in the `dist` folder.

## Requirements
- Windows 10 or later
- .NET 6.0 Runtime (download from Microsoft if needed)

## License
MIT