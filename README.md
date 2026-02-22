# Система мониторинга и управления поливом зеленых зон

Учебная программная система для мониторинга влажности почвы
и поддержки принятия решений о поливе.

## Структура проекта
```
irrigation-monitoring-system/
│
├── src/
│   ├── main.py
│   ├── config.py
│
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│
│   ├── services/
│   │   ├── sensor_service.py
│   │   ├── zone_service.py
│   │   └── irrigation_service.py
│
│   ├── analysis/
│   │   └── decision_engine.py
│
│   └── utils/
│       └── logger.py
│
├── data/
│   └── irrigation.db
│
├── docs/
│   ├── architecture.md
│   └── user_manual.md
│
├── README.md
├── .gitignore
└── requirements.txt
```
## Функциональность
- сбор данных с датчиков влажности
- работа с зонами полива
- анализ влажности
- рекомендации по поливу
- журнал событий

## Архитектура
Модульная, масштабируемая архитектура с разделением ответственности.

## Запуск
```bash
pip install -r requirements.txt
cd src
python main.py
```

## Установка на другом ПК (Windows)

1. Скопируйте репозиторий на целевой ПК.
2. Откройте PowerShell в каталоге проекта (корень, где лежит `install.ps1`).
3. Запустите:

```powershell
./install.ps1
```

Это создаст виртуальное окружение `.venv`, установит зависимости (если они появятся), создаст демонстрационные данные и запустит приложение.

## Установка на Linux/macOS

Откройте терминал в корне проекта и выполните:

```bash
./install.sh
```

## GUI application and packaging (Windows EXE)

I added a Tkinter GUI entry `app_gui.py` in the repository root. To run the GUI directly (no packaging):

```powershell
cd <repo-root>
python app_gui.py
```

To build a single-file Windows EXE, use `build_exe.ps1` (requires `pyinstaller`):

```powershell
./build_exe.ps1
```

The generated EXE will be in the `dist` folder as `IrrigationControlApp.exe`.

Notes:
- The GUI allows adding/removing sensors, adding measurements, simulating gas alarms and acknowledges.
- Packaging requires Python and `pyinstaller` (included in `requirements.txt`).

## Logs

- Text log: `logs/app.log` (rotating)
- Structured JSON lines: `logs/app.jsonl` (one JSON object per line)


## CI: Automatic build (GitHub Actions)

I've added a Windows CI workflow at `.github/workflows/build-windows.yml`. It performs:

- Checkout repository
- Set up Python 3.11
- Install dependencies from `requirements.txt`
- Build single-file EXE with `PyInstaller`
- (Optional) Install Inno Setup via Chocolatey and compile `installer.iss` to an installer
- Upload built EXE and installer as workflow artifacts

To enable installer creation the runner uses Chocolatey to install Inno Setup. If you prefer not to include the installer step, remove the Inno Setup steps from the workflow.

When the workflow completes, download artifacts from the Actions run to get `IrrigationControlApp.exe` and `IrrigationControlInstaller.exe`.

--
Если вы предпочитаете запускать вручную: можно выполнить из корня

```bash
python start.py
```

