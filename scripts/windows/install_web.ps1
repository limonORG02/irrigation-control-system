$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$venvPath = Join-Path $root ".venv"

Write-Host "[1/4] Создание виртуального окружения..."
python -m venv $venvPath

$pythonExe = Join-Path $venvPath "Scripts\python.exe"
if (-Not (Test-Path $pythonExe)) {
  throw "Python не найден в виртуальном окружении: $pythonExe"
}

Write-Host "[2/4] Установка зависимостей..."
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r (Join-Path $root "requirements.txt")

Write-Host "[3/4] Инициализация демо-данных..."
& $pythonExe (Join-Path $root "src\init_demo_data.py")

Write-Host "[4/4] Готово. Для запуска web-интерфейса используйте scripts\windows\run_web.bat"
