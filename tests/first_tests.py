from fastapi.testclient import TestClient

from fantasyappV2 import app
from sql_app import models
from sql_app.database import engine

client = TestClient(app)


def test_create_user():
    response = client.post("/api/create-user/", json={
        "name": "new-test-user1000",
        "password": "new-test-user1000",
        "email": "new-test-user1000@email.com",
        "squad_name": "test squad 2000"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "new-test-user1000"
    assert response.json()["email"] == "new-test-user1000@email.com"
    assert response.json()["is_active"]
    assert response.json()["squad_name"] == "test squad 2000"


def test_create_new_player():
    response = client.post("/api/create_player/", json={
        "name": "Roberto Inzaghi",
        "position": "DEF",
        "club": "AS ROMA",
        "cost": 123,
        "total_points": 200
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Roberto Inzaghi"
    assert response.json()["position"] == "DEF"
    assert response.json()["club"] == "AS ROMA"
    assert response.json()["cost"] == 123


def test_create_squads():
    response = client.post("/api/create_squads", json={
        "user_id": 1,
        "player_id": 1,
        "starter": True,
        "captain": True,
        "vice_captain": False
    })

    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    assert response.json()["player_id"] == 1
    assert response.json()["starter"]
    assert not response.json()["vice_captain"]
    assert response.json()["captain"]


def test_get_users():
    response = client.get("/api/get_users", params={
        "limit": 100,
        "skip": 0
    })

    assert response.status_code == 200
    assert response.json()[0]["name"] == "new-test-user1000"


def test_ok():
    response = client.get("/new_horison/")
    assert response.status_code == 200


def test_create_premierleague():
    response = client.get("/api/teams/premierleague/create/")
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_drop_db():
    models.Base.metadata.drop_all(bind=engine)
