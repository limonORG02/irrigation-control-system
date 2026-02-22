# PowerShell installer for Windows
Write-Host "Checking for Python..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3 and re-run." -ForegroundColor Red
    exit 1
}

Write-Host "Creating virtual environment .venv..."
python -m venv .venv

Write-Host "Upgrading pip and installing requirements..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Initializing database and running demo start..."
& .\.venv\Scripts\python.exe start.py

Write-Host "Installation complete."
