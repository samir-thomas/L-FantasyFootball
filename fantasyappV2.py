import typing

import sqlalchemy.orm
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from data.data import premierleague_club_list, create_list_schema
from sql_app import models
from sql_app.crud import get_league_details
from sql_app.database import engine
from sql_app.models import Player
from sql_app.schemas import SquadCreate
from squads.squad_validators import *
from squads.new_squad_1 import new_squad, assign_random_players_by_position

app = FastAPI()


def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


templates = Jinja2Templates(
    directory='templates', context_processors=[app_context], autoescape=False, auto_reload=True)

models.Base.metadata.create_all(bind=engine)


@app.get("/new_horison/")
async def read_main():
    return {"msg": "Hello World"}


@app.post("/api/create-user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    something = crud.create_user(db=db, user=user)
    print(something)
    return something


@app.post("/api/create_player/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)


# @app.post("/api/squad/add_single_player/", response_model=schemas.SquadCreate)
# def create_squad(squad: schemas.SquadCreate, db: Session = Depends(get_db)):
#     squad_capacity(squad=squad, db=db)
#     dup_check(squad=squad, db=db)
#     # starter_validators(squads=new_squad(GKP, DEF, MID, FWD, user_id=squad.user_id), db=db)
#     # dup_check(squad=squad, db=db)
#     db_squad = crud.add_player_to_squad_by_user(db=db, squad=squad)
#     print("db_squad", db_squad)
#     return db_squad


@app.get("/api/get_users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/")
async def homepage(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    context = {
        'request': request,
        "registered_users": crud.get_users(db, skip=skip, limit=limit)
    }
    print(crud.get_users(db, skip=skip, limit=limit))
    return templates.TemplateResponse('users.jinja2', context)


@app.get("/welcome_page_v3/{user_id}", response_class=HTMLResponse)
def welcome_page_v3(request: Request, user_id: int, db: Session = Depends(get_db)):
    context = {
        'request': request,
        'user_details': crud.get_user(db, user_id),
        'allocation': full_squad_allocation,
        'squad_details': crud.get_player_details_for_squad(db=db, user_id=user_id),
    }
    return templates.TemplateResponse('welcomeV3.jinja2', context)


@app.get("/api/squad/users/{user_id}", response_model=list[schemas.SquadPlayerUser])
def get_squad_details_for_user(user_id: int, db: Session = Depends(get_db)):
    player_schema_list = []
    squad_details = crud.get_player_details_for_squad(db=db, user_id=user_id)
    for player in squad_details:
        player_schema = schemas.SquadPlayerUser(player_id=player[1].player_id,
                                                user_id=player[1].user_id,
                                                starter=player[1].starter,
                                                captain=player[1].captain,
                                                vice_captain=player[1].vice_captain,
                                                position=player[0].position)
        player_schema_list.append(player_schema)
    return player_schema_list


# OLD implementation
@app.post("/api/squads/create/{user_id}", response_model=list[schemas.SquadCreate])
async def create_squad_for_user(user_id: int, db: Session = Depends(get_db)):
    # TODO: single function for validation
    # TODO: add persist after the validation checks pass
    # list of player_ids for building my squad
    # print(assign_random_squad(db=db, position="GKP"))
    GKP = assign_random_players_by_position(db=db, position="GKP")
    DEF = assign_random_players_by_position(db=db, position="DEF")
    MID = assign_random_players_by_position(db=db, position="MID")
    FWD = assign_random_players_by_position(db=db, position="FWD")
    print(GKP)
    print(DEF)
    print(MID)
    print(FWD)
    for squad_player in new_squad(GKP, DEF, MID, FWD, user_id=user_id):
        # squad_capacity_check(squad=squad_player, db=db)
        dup_check_db(squad=squad_player, db=db)
        validate_starting_players_in_each_position(player_list=new_squad(GKP, DEF, MID, FWD, user_id=user_id), db=db)
        crud.add_player_to_squad_by_user(db=db, squad=squad_player)

    return new_squad(GKP, DEF, MID, FWD, user_id=user_id)


@app.post("/api/squad/new/{user_id}", response_model=list[schemas.SquadPlayerId])
def create_new_squad_for_user(user_id: int, player_ids: list[schemas.SquadPlayerId],
                              db: Session = Depends(get_db)):
    squad_players = []
    # Validate schema

    # Get player details in order to validate the schema
    for squad_player_id in player_ids:
        player = crud.get_player_by_id(db=db, player_id=squad_player_id.player_id)
        squad_players.append(player)

    goalie = [current_player for current_player in squad_players if current_player.position == "GKP"]
    defense = [current_player for current_player in squad_players if current_player.position == "DEF"]
    midfield = [current_player for current_player in squad_players if current_player.position == "MID"]
    fwd = [current_player for current_player in squad_players if current_player.position == "FWD"]

    validate_position_allocation_for_squad(goalie, defense, midfield, fwd)

    for squad_player_id in player_ids:
        # Verify we can't over squad capacity ie 15 players
        squad_capacity_check(user_id=user_id, db=db)
        # Perform dup check on between schema and db
        crud.set_player_in_fresh_squad_for_user(db=db, user_id=user_id, player_id=squad_player_id.player_id)

    return player_ids


@app.post("/api/squad/starter/{user_id}", response_model=list[schemas.SquadCreate])
def set_starters_in_squad_for_user(user_id: int, player_ids: list[schemas.SquadPlayerId],
                                   db: Session = Depends(get_db)):
    player_schema_list = []

    if len(player_ids) != 11:
        raise HTTPException(status_code=400,
                            detail=f"You need to have 11 starters on the squad. you have selected {len(player_ids)}")

    validate_starting_players_in_each_position(player_ids, db=db)

    for player in player_ids:
        crud.set_starter_state_for_squad(db=db, user_id=user_id, player_id=player.player_id)

    my_squad = crud.get_squad_by_user_id(db=db, user_id=user_id)
    for player in my_squad:
        player_schema = schemas.SquadCreate(player_id=player.player.id,
                                            user_id=player.user_id,
                                            starter=player.starter,
                                            captain=player.captain,
                                            vice_captain=player.vice_captain)
        player_schema_list.append(player_schema)

    return player_schema_list


@app.post("/api/squad/set_captain/user/{user_id}/player_id/{player_id}", response_model=list[schemas.SquadCreate])
def set_team_captain(user_id: int, player_id: int, db: Session = Depends(get_db)):
    # Return 400 error if the player is not a starter
    squad_details = crud.get_player_details_for_squad(db=db, user_id=user_id)
    for player_details in squad_details:
        if player_details[1].player_id == player_id and not player_details[1].starter:
            raise HTTPException(status_code=400,
                                detail="Captain can only be assigned to a starter")
    player_schema_list = []
    my_squad = crud.get_squad_by_user_id(db=db, user_id=user_id)
    for player in my_squad:
        if player.captain and (player.player_id != player_id):
            # remove captain
            crud.set_captain_state_for_player(db=db, user_id=user_id, player_id=player.player_id, is_captain=False)
            print((player.player_id, "is no longer captain"))

    crud.set_captain_state_for_player(db=db, user_id=user_id, player_id=player_id, is_captain=True)

    my_squad_refreshed = crud.get_squad_by_user_id(db=db, user_id=user_id)
    for player in my_squad:
        player_schema = schemas.SquadCreate(player_id=player.player.id,
                                            user_id=player.user_id,
                                            starter=player.starter,
                                            captain=player.captain,
                                            vice_captain=player.vice_captain)
        player_schema_list.append(player_schema)
    return my_squad_refreshed


@app.post("/api/squad/set_vice_captain/user/{user_id}/player_id/{player_id}", response_model=list[schemas.SquadCreate])
def set_team_captain(user_id: int, player_id: int, db: Session = Depends(get_db)):
    # Return 400 error if the player is not a starter
    squad_details = crud.get_player_details_for_squad(db=db, user_id=user_id)
    for player_details in squad_details:
        if player_details[1].player_id == player_id and not player_details[1].starter and player_details[1].captain:
            raise HTTPException(status_code=400,
                                detail="Vice captain can only be assigned to a starter")
        if player_details[1].player_id == player_id and player_details[1].captain:
            raise HTTPException(status_code=400,
                                detail="player is already a captain")
    player_schema_list = []
    my_squad = crud.get_squad_by_user_id(db=db, user_id=user_id)
    for player in my_squad:
        if player.vice_captain and (player.player_id != player_id):
            # remove captain
            crud.set_vice_captain_state_for_player(db=db, user_id=user_id, player_id=player.player_id,
                                                   is_vice_captain=False)
            print((player.player_id, "is no longer vice captain"))

    crud.set_vice_captain_state_for_player(db=db, user_id=user_id, player_id=player_id, is_vice_captain=True)

    my_squad_refreshed = crud.get_squad_by_user_id(db=db, user_id=user_id)
    for player in my_squad:
        player_schema = schemas.SquadCreate(player_id=player.player.id,
                                            user_id=player.user_id,
                                            starter=player.starter,
                                            captain=player.captain,
                                            vice_captain=player.vice_captain)
        player_schema_list.append(player_schema)
    return my_squad_refreshed


@app.get("/api/players/create/{number_of_players}", response_model=list[schemas.Player])
async def api_create_random_players(db: Session = Depends(get_db), number_of_players: int | None = 1):
    players = crud.generate_random_players(db=db, number_of_players=number_of_players)
    return players


@app.get("/players/load")
def get_players_db(request: Request, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    context = {
        'request': request,
        'players_list': crud.get_players(db=db, skip=skip, limit=limit)
    }
    return templates.TemplateResponse('players_list_table.jinja2', context)


@app.get("/players/position/{position}", response_model=list[schemas.Player])
def get_players_db(db: Session = Depends(get_db), position: str | None = None):
    # context = {
    #     'request': request,
    #     'players_list': crud.get_players_by_position(db=db, postion=position)
    # }
    players = []
    # players = crud.get_players_by_position(db=db, position=position.upper())
    # players_in_position = [player for player in crud.get_players(db=db) if player.position == position]
    for player in crud.get_players(db=db):
        if player.position == position.upper():
            player_schema = schemas.Player(id=player.id,
                                           name=player.name,
                                           position=player.position,
                                           club=player.club,
                                           cost=player.cost,
                                           total_points=player.total_points)
            players.append(player_schema)
    return players


@app.post("/api/teams/league/create", response_model=list[schemas.ClubCreate])
def create_premierleague_teams(clubs: list[schemas.ClubCreate], league_name: str, db: Session = Depends(get_db)):
    added_clubs = []
    # league_name = 'premierleague'
    league_details = get_league_details(db=db, league=league_name)
    for club in clubs:
        this_club = crud.get_club_by_name_and_league(db, name=club.name, league=league_name)
        if not this_club:
            crud.insert_club(db=db, club=club, league_id=league_details.id)
            added_clubs.append(club)
            print(club)
    return clubs


@app.post("/api/league/create", response_model=schemas.League)
def create_league(league: schemas.League, db: Session = Depends(get_db)):
    return crud.add_league(db=db, league=league)
