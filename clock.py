"""
A simple analog clock system tray application.
Creates a minimalist clock icon in the system tray that updates every 10 seconds.
The clock shows hours with a line and minutes with a dot.
"""

from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw
import time
import math
from datetime import datetime
import os
import json
import webbrowser

GITHUB_URL = "https://github.com/adamstrandberg/analog-tray-clock"
PNG_ICON_PATH = "icon.png"  # PNG icon file for the executable

class ClockIcon:
    """Handles the creation and updating of the clock icon."""
    
    def __init__(self):
        self.size = 64  # Icon size in pixels
        self.center = self.size // 2
        self.radius = self.size // 2
        self.systray = None  # Will store the systray instance
        
        # Create app directory in user's home folder
        self.app_dir = os.path.join(os.path.expanduser('~'), '.clock_app')
        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)
        self.icon_path = os.path.join(self.app_dir, 'clock_icon.ico')
        self.config_path = os.path.join(self.app_dir, 'config.json')
        
        # Load or create theme configuration
        self.load_config()

    def create_clock_image(self):
        """Creates an analog clock image showing current time."""
        # Create transparent background
        image = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Set colors based on theme
        fg_color = 'black' if not self.dark_theme else 'white'
        
        # Get current time
        now = datetime.now()
        hours, minutes = now.hour, now.minute
        
        # Draw hour markers
        for i in range(12):
            angle = math.radians(i * 30 - 90)  # -90 to start at 12 o'clock
            dot_x = self.center + int(self.radius * 0.9375 * math.cos(angle))
            dot_y = self.center + int(self.radius * 0.9375 * math.sin(angle))
            draw.ellipse([dot_x-1, dot_y-1, dot_x+1, dot_y+1], fill=fg_color)
        
        # Draw hour hand
        hour_angle = math.radians((hours % 12 + minutes / 60) * 30 - 90)
        hour_x = self.center + int(self.radius * 0.75 * math.cos(hour_angle))
        hour_y = self.center + int(self.radius * 0.75 * math.sin(hour_angle))
        draw.line([self.center, self.center, hour_x, hour_y], fill=fg_color, width=4)
        
        # Draw minute marker
        minute_angle = math.radians(minutes * 6 - 90)
        minute_x = self.center + int(self.radius * 0.9375 * math.cos(minute_angle))
        minute_y = self.center + int(self.radius * 0.9375 * math.sin(minute_angle))
        draw.ellipse([minute_x-3, minute_y-3, minute_x+3, minute_y+3], fill=fg_color)
        
        # Save and handle any potential file system errors
        try:
            if os.path.exists(self.icon_path):
                os.remove(self.icon_path)
            image.save(self.icon_path, format='ICO')
        except Exception as e:
            print(f"Error saving icon: {e}")
            # Fallback to script directory if home directory is not accessible
            self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clock_icon.ico')
            image.save(self.icon_path, format='ICO')
            
        return self.icon_path

    def toggle_theme(self, systray):
        """Toggle between light and dark themes."""
        self.dark_theme = not self.dark_theme
        self.save_config()
        # Force immediate update of the icon
        icon_path = self.create_clock_image()
        self.systray.icon = icon_path
        # Force the system tray to refresh
        self.systray.update(hover_text="Analog Tray Clock", icon=icon_path)

    def get_windows_theme(self):
        """Detect if Windows is using dark theme."""
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseDarkTheme")
            return bool(value)
        except:
            return True  # Default to dark theme if can't detect

    def load_config(self):
        """Load theme configuration from file or create default."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.dark_theme = config.get('dark_theme', self.get_windows_theme())
            else:
                self.dark_theme = self.get_windows_theme()
                self.save_config()
        except:
            self.dark_theme = self.get_windows_theme()
        
    def save_config(self):
        """Save current theme configuration."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump({'dark_theme': self.dark_theme}, f)
        except:
            pass  # Ignore save errors

    def open_github(self, systray):
        """Open the GitHub repository in default browser."""
        webbrowser.open(GITHUB_URL)

def on_quit(systray):
    """Cleanup and exit the application."""
    try:
        if hasattr(systray, '_clock'):
            if os.path.exists(systray._clock.icon_path):
                os.remove(systray._clock.icon_path)
    except:
        pass  # Ignore cleanup errors on exit
    systray.shutdown()

def create_icon():
    """Create and run the system tray icon."""
    clock = ClockIcon()
    initial_icon = clock.create_clock_image()
    
    menu_options = (
        ("Toggle Theme", None, clock.toggle_theme),
        ("About Analog Tray Clock 1.0", None, clock.open_github),
    )
    systray = SysTrayIcon(initial_icon, "Analog Tray Clock", menu_options, on_quit=on_quit)
    clock.systray = systray
    systray._clock = clock
    systray.start()
    
    try:
        while True:
            new_icon = clock.create_clock_image()
            systray.update(hover_text="Analog Tray Clock", icon=new_icon)
            time.sleep(10)
    except KeyboardInterrupt:
        on_quit(systray)

if __name__ == '__main__':
    create_icon() 