using System.Drawing.Drawing2D;

namespace AnalogTrayClock;

internal class ClockApplicationContext : ApplicationContext
{
    private readonly NotifyIcon _notifyIcon;
    private readonly System.Windows.Forms.Timer _timer;
    private readonly ContextMenuStrip _contextMenu;
    private bool _isDarkTheme;
    private readonly string _configPath;
    private const string GITHUB_URL = "https://github.com/adamstrandberg/analog-tray-clock";

    public ClockApplicationContext()
    {
        // Set up configuration
        string appDataPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "AnalogTrayClock");
        
        Directory.CreateDirectory(appDataPath);
        _configPath = Path.Combine(appDataPath, "config.json");
        
        // Load theme setting
        LoadConfig();
        
        // Create context menu
        _contextMenu = new ContextMenuStrip();
        _contextMenu.Items.Add("Toggle Theme", null, ToggleTheme);
        _contextMenu.Items.Add("About Analog Tray Clock 1.1", null, OpenGitHub);
        _contextMenu.Items.Add("-"); // Separator
        _contextMenu.Items.Add("Exit", null, Exit);
        
        // Create notify icon
        _notifyIcon = new NotifyIcon
        {
            Text = "Analog Tray Clock",
            ContextMenuStrip = _contextMenu,
            Visible = true
        };
        
        // Create timer to update the clock every 10 seconds
        _timer = new System.Windows.Forms.Timer
        {
            Interval = 10000
        };
        _timer.Tick += (s, e) => UpdateClockIcon();
        
        // Initial update
        UpdateClockIcon();
        _timer.Start();
    }

    private void UpdateClockIcon()
    {
        using var icon = CreateClockIcon();
        _notifyIcon.Icon = icon;
    }

    private Icon CreateClockIcon()
    {
        // Create a bitmap in memory
        using var bitmap = new Bitmap(64, 64);
        using var graphics = Graphics.FromImage(bitmap);
        
        // Enable anti-aliasing
        graphics.SmoothingMode = SmoothingMode.AntiAlias;
        
        // Make background transparent
        graphics.Clear(Color.Transparent);
        
        // Set colors based on theme
        var fgColor = _isDarkTheme ? Color.White : Color.Black;
        
        // Get current time
        var now = DateTime.Now;
        var hours = now.Hour;
        var minutes = now.Minute;
        
        // Calculate center and radius
        int size = 64;
        int center = size / 2;
        int radius = size / 2;
        
        // Draw hour markers
        using var dotPen = new Pen(Color.FromArgb(192, fgColor), 2); // 75% opacity (192/255)
        for (int i = 0; i < 12; i++)
        {
            double angle = Math.PI * i / 6 - Math.PI / 2; // -90 degrees to start at 12 o'clock
            int dotX = center + (int)(radius * 0.9375 * Math.Cos(angle));
            int dotY = center + (int)(radius * 0.9375 * Math.Sin(angle));
            graphics.DrawEllipse(dotPen, dotX - 1, dotY - 1, 2, 2);
        }
        
        // Draw hour hand
        using var hourPen = new Pen(fgColor, 5);
        double hourAngle = Math.PI * ((hours % 12) + minutes / 60.0) / 6 - Math.PI / 2;
        int hourX = center + (int)(radius * 0.75 * Math.Cos(hourAngle));
        int hourY = center + (int)(radius * 0.75 * Math.Sin(hourAngle));
        graphics.DrawLine(hourPen, center, center, hourX, hourY);
        
        // Draw minute marker
        double minuteAngle = Math.PI * minutes / 30 - Math.PI / 2;
        int minuteX = center + (int)(radius * 0.9375 * Math.Cos(minuteAngle));
        int minuteY = center + (int)(radius * 0.9375 * Math.Sin(minuteAngle));
        using var minuteBrush = new SolidBrush(fgColor);
        graphics.FillEllipse(minuteBrush, minuteX - 5, minuteY - 5, 10, 10);
        
        return Icon.FromHandle(bitmap.GetHicon());
    }

    private void ToggleTheme(object? sender, EventArgs e)
    {
        _isDarkTheme = !_isDarkTheme;
        SaveConfig();
        UpdateClockIcon();
    }

    private void OpenGitHub(object? sender, EventArgs e)
    {
        System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo
        {
            FileName = GITHUB_URL,
            UseShellExecute = true
        });
    }

    private void Exit(object? sender, EventArgs e)
    {
        // Clean up
        _timer.Stop();
        _notifyIcon.Visible = false;
        Application.Exit();
    }

    private void LoadConfig()
    {
        try
        {
            if (File.Exists(_configPath))
            {
                string json = File.ReadAllText(_configPath);
                var options = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, bool>>(json);
                if (options != null && options.TryGetValue("dark_theme", out bool darkTheme))
                {
                    _isDarkTheme = darkTheme;
                    return;
                }
            }
            
            // Default to system setting if config doesn't exist
            _isDarkTheme = IsSystemUsingDarkTheme();
        }
        catch
        {
            _isDarkTheme = IsSystemUsingDarkTheme();
        }
    }

    private void SaveConfig()
    {
        try
        {
            var options = new Dictionary<string, bool> { { "dark_theme", _isDarkTheme } };
            string json = System.Text.Json.JsonSerializer.Serialize(options);
            File.WriteAllText(_configPath, json);
        }
        catch
        {
            // Ignore save errors
        }
    }

    private bool IsSystemUsingDarkTheme()
    {
        try
        {
            using var key = Microsoft.Win32.Registry.CurrentUser.OpenSubKey(
                @"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize");
            
            if (key?.GetValue("AppsUseDarkTheme") is int value)
            {
                return value == 1;
            }
        }
        catch
        {
            // Ignore registry errors
        }
        
        return true; // Default to dark theme if detection fails
    }
} 