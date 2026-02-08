@echo off
setlocal
set ROOT=%~dp0..\..
set VENV=%ROOT%\.venv
set PYTHON=%VENV%\Scripts\python.exe

if not exist "%PYTHON%" (
  echo Виртуальное окружение не найдено. Запустите scripts\windows\install_web.ps1
  exit /b 1
)

"%PYTHON%" "%ROOT%\src\web\app.py"
endlocal
