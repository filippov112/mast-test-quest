# 🖥️ Клиент-серверное приложение на FastAPI + PySide6

## 📌 Описание

Приложение состоит из:
- **Сервера на FastAPI**, принимающего POST-запросы с данными и возвращающего список сохранённых записей (с пагинацией)
- **Клиента на PySide6**, позволяющего отправлять текст и просматривать список записей в графическом интерфейсе

Данные сохраняются в SQLite (отдельно для продакшена и тестов).

---

## 🗂️ Структура проекта

```
project/
│
├── client/               # GUI-клиент на PySide6
│   └── main.py
│
├── dist/               # GUI-клиент на PySide6
│   ├── server_app/
│   │   └── server_app.exe # Исполняемый файл сервера
│   └── client_app.exe     # Исполняемый файл клиента
│
├── server/               # FastAPI сервер и логика БД
│   ├── main.py           # Эндпоинты
│   ├── crud.py           # Операции с БД
│   ├── models.py         # SQLAlchemy-модель
│   ├── schemas.py        # Pydantic-схемы
│   └── database.py       # Подключение и сессии
│
├── tests/                # Юнит-тесты клиента и сервера
│   ├── test\_client.py
│   └── test\_main.py
│
├── records.db            # Боевая база данных (создаётся при первом запуске)
└── README.md
```

---

## 🚀 Запуск

1. Установить зависимости

    ```bash
    pip install -r requirements.txt
    ```

3. Запустить сервер:
    ```bash
    uvicorn server.main:app --reload
    ```
    Доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    Документация Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
<br>
4. Запустить клиент:
    ```bash
    python client/main.py
    ```

---

### 📦 Сборка клиента

Для сборки standalone-версии клиента:

```bash
pyinstaller --name client_app --onefile --windowed client/main.py
```

* `--onefile` — создаёт один `.exe` файл
* `--windowed` — отключает консоль (для GUI)

Готовый исполняемый файл появится в папке `dist/`:

```
dist/
└── client_app.exe
```

---

### 📦 Сборка сервера

Для упаковки сервера в отдельную папку:

```bash
pyinstaller --name server_app --onedir server/main.py
```

* `--onedir` — создаёт папку с исполняемым файлом и зависимостями (удобно для разработки и отладки)

В папке `dist/server_app/` появится исполняемый файл и все необходимые библиотеки.

---

## 🧪 Тестирование

Тесты запускаются с использованием `unittest` и `FastAPI TestClient`.
```bash
pytest
```
Все тесты используют in-memory SQLite базу (отдельно от боевой).

---

## 📤 Эндпоинты сервера

* `POST /submit` — принимает JSON с текстом, датой, временем и номером клика
* `GET /records` — возвращает список записей, поддерживает пагинацию (`skip`, `limit`)

---

## 🧱 Пример записи в базе

```json
{
  "id": 1,
  "text": "Пример",
  "date": "2025-06-17",
  "time": "14:00:00",
  "click_number": 3
}
```

---

## 🛠️ Используемые технологии

* Python 3.11
* FastAPI / Pydantic / SQLAlchemy / sqlite3
* PySide6
* requests
* unittest / mock
