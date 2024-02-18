import faker.generator
import pytest
import requests
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

import fantasyappV2
from fantasyappV2 import *
from sql_app import models, crud
from sql_app.crud import *
from sql_app.database import engine, SQLALCHEMY_DATABASE_URL, Base
from sql_app.db import get_db
from unittest.mock import *

from sql_app.models import User

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# app.dependency_overrides[schemas.UserCreate] = existing_users

client = TestClient(app)

pos_gkp = "GKP"
pos_def = "DEF"
pos_mid = "MID"
pos_fwd = "FWD"


@pytest.fixture()
def pre_populated_user(db_session):
    user_schema_example = \
        User(name="samir",
             hashed_password="samir101",
             email="samir@example.com",
             squad_name="the samis"
             )
    db_session.add(user_schema_example)
    db_session.commit()
    db_session.refresh(user_schema_example)
    db_session.close()
    return user_schema_example


@pytest.fixture()
def new_user(db_session):
    email = f"new-test-user{randint(1, 3000)}@email.com"
    new_user_schema = \
        User(name="new_user",
             hashed_password="samir101",
             email=email,
             squad_name="new_user_squad_example"
             )
    db_session.add(new_user_schema)
    db_session.commit()
    db_session.refresh(new_user_schema)
    db_session.close()
    return new_user_schema


@pytest.fixture()
def new_player(db_session):
    new_player_schema = models.Player(
        name="the GOAT",
        position=pos_mid,
        club="Fulham FC",
        cost=300,
        total_points=250
    )
    db_session.add(new_player_schema)
    db_session.commit()
    db_session.refresh(new_player_schema)
    db_session.close()
    return new_player_schema


@pytest.fixture()
def set_premierleague(db_session):
    new_league_schema = models.League(
        name="premierleague",
        league_size=20
    )
    db_session.add(new_league_schema)
    db_session.commit()
    db_session.refresh(new_league_schema)
    db_session.close()
    return new_league_schema


@pytest.fixture()
def mock_league_teams():
    teams = [
        {"name": "Bournemouth"},
        {"name": "Arsenal"},
        {"name": "Aston Villa"},
        {"name": "Brentford"},
        {"name": "Brighton"},
        {"name": "Burnley"}
    ]
    return teams


# @pytest.mark.skip(reason="WIP")
def test_get_a_user_by_email(db_session, pre_populated_user):
    # Arrange
    # seed_data(db_session, existing_users)
    test_user = db_session.query(models.User).filter(models.User.email == pre_populated_user.email).first()
    expect_response = {
        'email': pre_populated_user.email,
        'id': test_user.id,
        'is_active': True,
        'name': pre_populated_user.name
    }

    # Act
    response = client.get("/api/get_users", params={
        "limit": 100,
        "skip": 0
    })

    # Assert
    assert response.status_code == 200
    user_list = [user for user in response.json() if user["email"] == expect_response["email"]]
    assert len(user_list) == 1
    for user in response.json():
        if user["email"] == expect_response["email"]:
            assert user["id"] == expect_response["id"]
            assert user["is_active"] == expect_response["is_active"]
            assert user["name"] == expect_response["name"]


def test_create_new_player():
    response = client.post("/api/create_player/", json={
        "name": "Roberto Inzaghi",
        "position": pos_def,
        "club": "AS ROMA",
        "cost": 123,
        "total_points": 200
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Roberto Inzaghi"
    assert response.json()["position"] == pos_def
    assert response.json()["club"] == "AS ROMA"
    assert response.json()["cost"] == 123


# def test_add_player_to_a_squad(db_session, new_user, new_player):
#     # Arrange
#     test_user = db_session.query(models.User).filter(models.User.email == new_user.email).first()
#     test_player = db_session.query(models.Player)\
#         .filter(models.Player.name == new_player.name
#                 and models.Player.position == new_player.position).first()
#
#     user_id = test_user.id
#     player_id = test_player.id
#
#     # Act
#     response = client.post("/api/squad/add_single_player/", json={
#         "user_id": user_id,
#         "player_id": player_id,
#         "starter": True,
#         "captain": True,
#         "vice_captain": False
#     })
#
#     # Assert
#     assert response.status_code == 200
#     assert response.json()["user_id"] == user_id
#     assert response.json()["player_id"] == player_id
#     assert response.json()["starter"] is True
#     assert response.json()["vice_captain"] is False
#     assert response.json()["captain"] is True


def test_add_teams_to_league(set_premierleague, mock_league_teams):
    response = client.post("/api/teams/league/create/", params={
                "league_name": "premierleague"
                }, json=mock_league_teams)

    assert response.status_code == 200
    assert len(response.json()) == 6
