import time
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from dop_zhu_zad.main import app, get_db
from dop_zhu_zad.database import Base, engine

# Создаем тестовую базу данных
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        print("New db")
        yield db
    finally:
        print("db closed")
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Тесты API
def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_token():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

    return response.json()["access_token"]

def test_get_bonus_data():
    access_token = test_get_token()
    response = client.get(
        "/bonus",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert "current_level" in response.json()

def test_create_transaction():
    access_token = test_get_token()
    response = client.post(
        "/transactions/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"amount": 1200.0},
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_token_expiration():
    access_token = test_get_token()
    response = client.get(
        "/bonus",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    time.sleep(65)

    response = client.get(
        "/bonus",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401
