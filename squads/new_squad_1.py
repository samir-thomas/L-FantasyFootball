import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from sql_app import schemas, crud
from squads.squad_validators import full_squad_allocation, starter_allocation


def assign_random_players_by_position(db: Session, position):
    all_players = crud.get_players(db=db, skip=0, limit=200)
    players_in_position = [player for player in all_players if player.position == position]
    squad_player = []
    count = 0
    while count < full_squad_allocation[position]:
        new_player = random.choice(players_in_position)
        if new_player not in squad_player:
            squad_player.append(new_player.id)
            players_in_position.remove(new_player)  # prevents having duplicates in the chosen squad
            count = count + 1

    return squad_player


def new_squad(goalkeeper, defence, midfield, forward, user_id):
    player_1 = schemas.SquadCreate(
        user_id=user_id,
        player_id=goalkeeper[0],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_2 = schemas.SquadCreate(
        user_id=user_id,
        player_id=goalkeeper[1],
        starter=False,
        captain=False,
        vice_captain=False
    )
    player_3 = schemas.SquadCreate(
        user_id=user_id,
        player_id=defence[0],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_4 = schemas.SquadCreate(
        user_id=user_id,
        player_id=defence[1],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_5 = schemas.SquadCreate(
        user_id=user_id,
        player_id=defence[2],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_6 = schemas.SquadCreate(
        user_id=user_id,
        player_id=defence[3],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_7 = schemas.SquadCreate(
        user_id=user_id,
        player_id=defence[4],
        starter=False,
        captain=False,
        vice_captain=False
    )
    player_8 = schemas.SquadCreate(
        user_id=user_id,
        player_id=midfield[0],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_9 = schemas.SquadCreate(
        user_id=user_id,
        player_id=midfield[1],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_10 = schemas.SquadCreate(
        user_id=user_id,
        player_id=midfield[2],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_11 = schemas.SquadCreate(
        user_id=user_id,
        player_id=midfield[3],
        starter=True,
        captain=True,
        vice_captain=False
    )
    player_12 = schemas.SquadCreate(
        user_id=user_id,
        player_id=midfield[4],
        starter=False,
        captain=False,
        vice_captain=False
    )
    player_13 = schemas.SquadCreate(
        user_id=user_id,
        player_id=forward[0],
        starter=True,
        captain=False,
        vice_captain=True
    )
    player_14 = schemas.SquadCreate(
        user_id=user_id,
        player_id=forward[1],
        starter=True,
        captain=False,
        vice_captain=False
    )
    player_15 = schemas.SquadCreate(
        user_id=user_id,
        player_id=forward[2],
        starter=False,
        captain=False,
        vice_captain=False
    )

    if len(goalkeeper) > full_squad_allocation["GKP"] \
            or len(defence) > full_squad_allocation["DEF"] \
            or len(midfield) > full_squad_allocation["MID"] \
            or len(forward) > full_squad_allocation["FWD"]:
        raise HTTPException(status_code=400,
                            detail=f"You have exceeded capacity for one of your positions, "
                                   f"you have {len(goalkeeper)}, {len(defence)}, {len(midfield)}")

    squad_schemas = [player_1, player_2, player_3, player_4, player_5,
                     player_6, player_7, player_8, player_9, player_10,
                     player_11, player_12, player_13, player_14, player_15]

    captains = [squad for squad in squad_schemas if squad.captain]
    vice_captains = [squad for squad in squad_schemas if squad.vice_captain]
    starters = [squad for squad in squad_schemas if squad.starter]

    if len(captains) == 0:
        raise HTTPException(status_code=400,
                            detail="Please assign a captain to your squad")
    if len(captains) > 1:
        raise HTTPException(status_code=400,
                            detail="You cannot have more than 1 captain")

    if len(vice_captains) == 0:
        raise HTTPException(status_code=400,
                            detail="Please assign a vice captain to your squad")

    if len(vice_captains) > 1:
        raise HTTPException(status_code=400,
                            detail="Cannot have more than 1 vice captain")

    if len(starters) != 11:
        raise HTTPException(status_code=400,
                            detail=f"You need to have 11 starters on the squad. you have selected {len(starters)}")
    for cap in captains:
        if cap.captain and not cap.starter:
            raise HTTPException(status_code=400,
                                detail=f"Your captain needs to be a starter")

    for vcap in vice_captains:
        if vcap.captain and not vcap.starter:
            raise HTTPException(status_code=400,
                                detail=f"Your vice captain needs to be a starter")

    for squad in squad_schemas:
        if squad.captain and squad.vice_captain:
            raise HTTPException(status_code=400,
                                detail=f"You cannot assign captain and vice captain to the same player")

    return squad_schemas

