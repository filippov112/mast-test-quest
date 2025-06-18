from datetime import date
from fastapi.testclient import TestClient
from server.database import Base, engine_test, TestingSessionLocal
from server.main import app, get_db

# Подмена зависимости
def override_get_db():
    print("✅ Используется ТЕСТОВАЯ база")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Создаём таблицы в in-memory базе
Base.metadata.drop_all(bind=engine_test)
Base.metadata.create_all(bind=engine_test)

client = TestClient(app)

def test_submit_record():
    """Проверяет успешную отправку записи через POST /submit и корректность возвращаемых данных."""

    payload = {
        "text": "тестовая запись",
        "date": str(date.today()),
        "time": "12:00:00",
        "click_number": 1
    }
    response = client.post("/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == payload["text"]
    assert data["click_number"] == payload["click_number"]

def test_get_records_default_pagination():
    """Проверяет успешный GET-запрос к /records с параметрами по умолчанию и тип возвращаемых данных."""

    response = client.get("/records")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_records_with_pagination():
    """Проверяет GET-запрос к /records с явно заданными skip и limit, убеждается, что возвращается список."""

    response = client.get("/records?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
