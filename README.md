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

