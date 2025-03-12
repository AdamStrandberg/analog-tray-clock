# Build script for Analog Tray Clock - Small Version
Write-Host "Building small executable..."

# First, stop any running instances
Stop-Process -Name AnalogTrayClock -Force -ErrorAction SilentlyContinue

# Create a framework-dependent version (smaller, requires .NET runtime)
Write-Host "Creating framework-dependent executable (requires .NET runtime)..."
dotnet publish -c Release -r win-x64 --self-contained false -p:PublishSingleFile=true

# Create dist folder if it doesn't exist
$distDir = "./dist"
if (-not (Test-Path $distDir)) {
    New-Item -ItemType Directory -Path $distDir | Out-Null
}

# Copy the executable to dist folder
$exePath = "bin\Release\net6.0-windows\win-x64\publish\AnalogTrayClock.exe"
$destPath = "$distDir\AnalogTrayClock.exe"

Copy-Item $exePath -Destination $destPath -Force

# Get file size
$fileSize = [Math]::Round((Get-Item $destPath).Length / 1MB, 2)

Write-Host "Build complete!"
Write-Host "-----------------------------"
Write-Host "Executable created at: $destPath"
Write-Host "File size: $fileSize MB"
Write-Host "Requires .NET 6.0 Runtime"
Write-Host "-----------------------------" 