# Система мониторинга и управления поливом зеленых зон

Учебная программная система для мониторинга влажности почвы
и поддержки принятия решений о поливе.

## Структура проекта
```
irrigation-control-system/
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── init_demo_data.py
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
│   ├── utils/
│   │   └── logger.py
│   │
│   └── web/
│       ├── app.py
│       └── templates/
│           └── index.html
│
├── data/
│   └── irrigation.db
│
├── scripts/
│   └── windows/
│       ├── install_web.ps1
│       └── run_web.bat
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
python src/main.py
```

## Запуск web-интерфейса
```bash
pip install -r requirements.txt
python src/init_demo_data.py
python src/web/app.py
```

Откройте в браузере: http://localhost:5000

## Запуск web-интерфейса (Windows)
1. Откройте PowerShell в корне проекта.
2. Запустите установочный скрипт:
```powershell
scripts\\windows\\install_web.ps1
```
3. Для запуска web-интерфейса используйте:
```powershell
scripts\\windows\\run_web.bat
```

Если скрипт PowerShell блокируется политикой безопасности, выполните:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Измененные и добавленные файлы
- обновлены: `src/config.py`, `src/main.py`, `src/services/zone_service.py`, `src/web/templates/index.html`, `README.md`
- добавлены: `src/web/app.py`, `requirements.txt`, `scripts/windows/install_web.ps1`, `scripts/windows/run_web.bat`
