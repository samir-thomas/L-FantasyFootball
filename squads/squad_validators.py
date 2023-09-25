from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sql_app import schemas, crud
from sql_app.db import get_db

allocation = {
    "GKP": 2,
    "DEF": 5,
    "MID": 5,
    "FWD": 3,
}

starter_allocation = {
    "GKP": 1,
    "DEF": 5,
    "MID": 5,
    "FWD": 3
}


def dup_check(squad: schemas.SquadCreate, db: Session = Depends(get_db)):
    my_current_squad = crud.get_squad_by_user_id(db=db, user_id=squad.user_id)
    for sq_player in my_current_squad:
        if sq_player:
            if sq_player.user_id == squad.user_id and sq_player.player_id == squad.player_id:
                raise HTTPException(status_code=400,
                                    detail=f'player_id: {squad.player_id}' + " already exists in your squad")


def squad_capacity(squad: schemas.SquadCreate, db: Session = Depends(get_db)):
    my_current_squad = crud.get_squad_by_user_id(db=db, user_id=squad.user_id)
    if len(my_current_squad) >= 15:
        raise HTTPException(status_code=400,
                            detail="Squad limit reached")


def starter_validators(squads, db: Session = Depends(get_db())):
    unique_positions = ["GKP", "DEF", "MID", "FWD"]
    for position in unique_positions:
        player_count = [player for player in squads
                        if crud.get_player_by_id(db=db,
                                                 player_id=player.player_id).position == position
                        and player.starter]
        if len(player_count) > starter_allocation[position]:
            raise HTTPException(status_code=400,
                                detail=f"Only {starter_allocation[position]} {position} allowed for a single match")
