# Build EXE using PyInstaller (Windows)
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Install Python 3." -ForegroundColor Red
    exit 1
}

python -m pip install --upgrade pip
python -m pip install pyinstaller

# Build single-file windowed exe
pyinstaller --noconsole --onefile app_gui.py --name IrrigationControlApp

Write-Host "Build finished. Check the 'dist' folder." -ForegroundColor Green
