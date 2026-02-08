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

## Измененные и добавленные файлы
- обновлены: `src/config.py`, `src/main.py`, `src/services/zone_service.py`, `README.md`
- добавлены: `src/web/app.py`, `src/web/templates/index.html`, `requirements.txt`
