from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from sql_app import schemas, crud
from sql_app.db import get_db

full_squad_allocation = {
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


def dup_check_db(squad: schemas.SquadCreate, db: Session = Depends(get_db)):
    my_current_squad = crud.get_squad_by_user_id(db=db, user_id=squad.user_id)
    for sq_player in my_current_squad:
        if sq_player:
            if sq_player.user_id == squad.user_id and sq_player.player_id == squad.player_id:
                raise HTTPException(status_code=400,
                                    detail=f'player_id: {squad.player_id}' + " already exists in your squad")


# TODO: fix
# def dup_check_data(player_ids):
#     for playerId in player_ids:
#         if player_ids.count(playerId) > 1:
#             raise HTTPException(status_code=400,
#                                 detail=f'player_id: {player.player_id}' + " already exists in your squad")


def squad_capacity_check(user_id: int, db: Session = Depends(get_db)):
    my_current_squad = crud.get_squad_by_user_id(db=db, user_id=user_id)
    if len(my_current_squad) >= 15:
        raise HTTPException(status_code=400,
                            detail="Squad limit reached")
    return my_current_squad


def validate_starting_players_in_each_position(player_list, db: Session = Depends(get_db())):
    unique_positions = ["GKP", "DEF", "MID", "FWD"]
    for position in unique_positions:
        players_in_position = [player for player in player_list
                               if crud.get_player_by_id(db=db,
                                                        player_id=player.player_id).position == position]
                               # and player.starter]
        if len(players_in_position) > starter_allocation[position]:
            raise HTTPException(status_code=400,
                                detail=f"Only {starter_allocation[position]} {position} allowed for a single match")
    return True


def validate_position_allocation_for_squad(goalkeeper, defence, midfield, forward):
    if len(goalkeeper) > full_squad_allocation["GKP"] \
            or len(defence) > full_squad_allocation["DEF"] \
            or len(midfield) > full_squad_allocation["MID"] \
            or len(forward) > full_squad_allocation["FWD"]:
        raise HTTPException(status_code=400,
                            detail=f"You have exceeded capacity for one of your positions, "
                                   f"you have {len(goalkeeper)} goalkeepers, "
                                   f"{len(defence)} defenders, "
                                   f"{len(midfield)} midfielders, "
                                   f"{len(forward)} forwards ")
    return True
