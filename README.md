# BusInfoHack

Проект для анализа загруженности автобусов по данным с камер.  
Серверная часть реализована на **FastAPI** + **PostgreSQL**, миграции — **yoyo**.  
Цель — собирать данные с камер в салоне автобуса, хранить в БД и предоставлять API для фронтенда.

---

## Структура проекта

```
├── apps/
│   ├── api/            # FastAPI-приложение
│   │   ├── main.py
│   │   ├── router.py
│   │   └── schemas.py
│   └── ingest/         # (будущий сервис сбора данных)
├── database/
│   ├── managers/       # Логика работы с таблицами
│   ├── models/         # Модели таблиц
│   └── async_db.py     # Основные методы для работы с базой данных
├── migrations/         # yoyo миграции
├── utils/              # config, logger
├── compose.yml
├── Dockerfile
├── Makefile
└── README.md
```

---

## Запуск в Docker

1. Собрать и запустить контейнеры:
   ```bash
   make startup
   ```

2. API будет доступно на: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   БД — на порту `5433` с хоста (`localhost:5433`).

---

## Makefile команды

- `make core` — запустить только Postgres
- `make build` — собрать сервис `bus-api`
- `make up` — запустить API (и Postgres если не запущен)
- `make down` — остановить и удалить контейнеры
- `make ps` — список контейнеров
- `make logs` — логи сервисов
- `make migrate` — применить миграции
- `make rollback` — откатить одну миграцию
- `make migrate_reload` — полный цикл
- `make startup` — полный запуск + миграции

---

## Примеры API

### Список автобусов

```
GET /api/buses
```

### Загруженность по нескольким автобусам

```
GET /api/bus/now?device_ids=102&device_ids=120
```

### Средняя загруженность по маршруту

```
GET /api/route/avg/{route_id}
```
