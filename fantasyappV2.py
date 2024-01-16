import typing

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from data.data import premierleague_club_list, create_list_schema
from sql_app import models
from sql_app.crud import get_league_details
from sql_app.database import engine
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


@app.post("/api/create_squads/", response_model=schemas.SquadCreate)
def create_squad(squad: schemas.SquadCreate, db: Session = Depends(get_db)):
    dup_check(squad=squad, db=db)
    db_squad = crud.add_player_to_squad_by_user(db=db, squad=squad)
    print("db_squad", db_squad)
    return db_squad


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
        'allocation': allocation,
        'squad_details': crud.get_player_details_for_squad(db=db, user_id=user_id),
    }
    return templates.TemplateResponse('welcomeV3.jinja2', context)


@app.post("/api/squads/create/{user_id}", response_model=list[schemas.SquadCreate])
async def create_squad_for_user(user_id: int, db: Session = Depends(get_db)):
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
        squad_capacity(squad=squad_player, db=db)
        dup_check(squad=squad_player, db=db)
        starter_validators(squads=new_squad(GKP, DEF, MID, FWD, user_id=user_id), db=db)
        crud.add_player_to_squad_by_user(db=db, squad=squad_player)

    return new_squad(GKP, DEF, MID, FWD, user_id=user_id)


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
    return added_clubs


@app.post("/api/league/create", response_model=schemas.League)
def create_league(league: schemas.League, db: Session = Depends(get_db)):
    return crud.add_league(db=db, league=league)
