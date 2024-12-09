"""
Build script for the clock application.
Handles both building the executable and setting up autostart.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Build new executable
    subprocess.run([
        'python', '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name=AnalogTrayClock',
        '--icon=icon.png',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=scipy',
        '--exclude-module=tkinter',
        '--exclude-module=PyQt5',
        '--exclude-module=PySide2',
        '--exclude-module=wx',
        '--exclude-module=pydoc',
        '--exclude-module=doctest',
        '--exclude-module=unittest',
        '--exclude-module=test',
        '--exclude-module=distutils',
        '--noupx',
        'clock.py'
    ], check=True)
    
    print("Build completed successfully!")
    return os.path.join('dist', 'AnalogTrayClock.exe')

def main():
    """Main build process."""
    try:
        # Install requirements
        print("Installing requirements...")
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        
        # Build executable
        exe_path = build_executable()
        
        print("\nBuild and setup completed successfully!")
        print(f"Executable location: {os.path.abspath(exe_path)}")
        
    except Exception as e:
        print(f"Error during build process: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 