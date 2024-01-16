from sqlalchemy.orm import Session
from random import *
from utils.randomiser import *
from sql_app import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email,
                          hashed_password=fake_hashed_password,
                          name=user.name,
                          squad_name=user.squad_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_players(db: Session, skip: int = 0, limit: int = 500):
    return db.query(models.Player).offset(skip).limit(limit).all()


def get_player_by_name(db: Session, player_name: str):
    return db.query(models.Player).filter(models.Player.name == player_name).first()


def get_player_by_id(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def generate_random_players(db: Session, number_of_players):
    db_players = []
    for num in range(number_of_players):
        random_db_club = get_random_club(db)
        db_player = models.Player(name=assign_random_player_name(),
                                  position=assign_player_position(),
                                  club=random_db_club,
                                  cost=assign_cost(),
                                  total_points=assign_points_total())
        db.add(db_player)
        db_players.append(db_player)
        db.commit()
        db.refresh(db_player)
    return db_players


def get_club_by_name_and_league(db: Session, name: str, league: str):
    return db.query(models.Club, models.League)\
        .join(models.League)\
        .filter(models.Club.name == name and models.League.name == league).first()


def get_league_details(db: Session, league: str):
    league_details = db.query(models.League).filter(models.League.name == league).first()
    return league_details


def add_league(db: Session, league: schemas.League):
    db_league = models.League(
        **league.model_dump()
    )
    db.add(db_league)
    db.commit()
    db.refresh(db_league)
    return db_league


def get_random_club(db: Session, skip: int = 0, limit: int = 20):
    all_clubs = db.query(models.Club).offset(skip).limit(limit).all()
    random_club = random.choice(all_clubs)
    return random_club.name


def insert_club(db: Session, club: schemas.ClubCreate, league_id):
    db_club = models.Club(name=club.name,
                          league_id=league_id)
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club


def get_squad_by_user_id(db: Session, user_id: int):
    return db.query(models.Squad).filter(models.Squad.user_id == user_id).all()


def add_player_to_squad_by_user(db: Session, squad: schemas.SquadCreate):
    db_squad = models.Squad(user_id=squad.user_id,
                            player_id=squad.player_id,
                            starter=squad.starter,
                            captain=squad.captain,
                            vice_captain=squad.vice_captain
                            )
    db.add(db_squad)
    db.commit()
    db.refresh(db_squad)
    return db_squad


def get_players_by_position(db: Session, position):
    return db.query(models.Player) \
        .filter(models.Player.position == position).all()


def get_player_details_for_squad(db: Session, user_id):
    return db.query(models.Player, models.Squad, models.User) \
        .join(models.Squad, models.Squad.player_id == models.Player.id) \
        .join(models.User, models.User.id == models.Squad.user_id) \
        .filter(models.Squad.user_id == user_id).all()

