# API Service

Backend-сервис проекта **BusFullness** — предоставляет REST API для приёма данных от камер, работы с базой данных и
отображения информации о загруженности транспорта

---

## Основные возможности

- Приём и обработка данных от устройств (ESP32)
- Сохранение и агрегация данных о пассажиропотоке
- REST API для фронтенда и браузерного расширения
- Интеграция с PostgreSQL
- Поддержка миграций и контейнеризации (Docker)

---

## Структура проекта

```text
api/
├── apps/
│   └── api/
│       ├── routers/                # Эндпоинты FastAPI
│       │   ├── __init__.py
│       │   ├── buses.py            # Работа с автобусами
│       │   ├── cameras.py          # Управление камерами
│       │   ├── measurements.py     # Сырые измерения и данные от устройств
│       │   ├── routes_avg.py       # Средние данные по маршрутам
│       │   └── snapshots.py        # Снимки состояния
│       │
│       ├── schemas/                # Pydantic-схемы
│       │   ├── __init__.py
│       │   ├── buses.py
│       │   ├── cameras.py
│       │   ├── measurements.py
│       │   ├── routes.py
│       │   └── snapshots.py
│       │
│       ├── deps.py                 # Зависимости для DI FastAPI
│       └── main.py                 # Точка входа приложения
│
├── database/                       # Работа с БД
│   ├── managers/                   # Логика управления сущностями
│   │   ├── __init__.py
│   │   ├── bus_manager.py
│   │   ├── camera_manager.py
│   │   └── info_from_camera_manager.py
│   │
│   ├── models/                     # SQLAlchemy-модели
│   │   ├── __init__.py
│   │   ├── bus.py
│   │   ├── camera.py
│   │   ├── info_from_camera.py
│   │   └── async_db.py
│   │
│   └── migrations/                 # SQL-миграции
│       ├── 001.init.sql
│       ├── 001.init.rollback.sql
│       ├── 002.add_data.sql
│       └── 002.add_data.rollback.sql
│
├── utils/                          # Вспомогательные модули
│   ├── __init__.py
│   ├── config.py                   # Работа с конфигурацией
│   └── logger.py                   # Настройка логирования
│
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## Быстрый старт

1. Скопируйте шаблон окружения:
   ```bash
   cp .env.example .env
   ```

2. Укажите свои настройки (БД, порты и т.д.)

3. Убедитесь, что установлены необходимые инструменты:
    - `make` — для запуска инфраструктуры
    - зависимости из `requirements.txt` — для миграций и вспомогательных скриптов

4. Запустите инфраструктуру:
   ```bash
   make startup
   ```

5. После успешного запуска:
    - API доступно по адресу: [http://127.0.0.1:8000/docs](http://localhost:8000/docs)
    - PostgreSQL доступна локально на порту, указанном в `.env`

---

## Документация API

Подробная интерактивная документация доступна в Swagger UI после запуска приложения:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Также доступна альтернативная версия в формате ReDoc:  
👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---
