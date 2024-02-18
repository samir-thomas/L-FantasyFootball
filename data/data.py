from sql_app import schemas, crud

league_name = 'premierleague'

schema_create_example = [
    {"name": "Bournemouth"},
    {"name": "Arsenal"},
    {"name": "Aston Villa"},
    {"name": "Brentford"},
    {"name": "Brighton"},
    {"name": "Burnley"},
    {"name": "Chelsea"},
    {"name": "Crystal Palace"},
    {"name": "Everton"},
    {"name": "Fulham"},
    {"name": "Liverpool"},
    {"name": "Luton Town"},
    {"name": "Manchester City"},
    {"name": "Manchester United"},
    {"name": "Newcastle United"},
    {"name": "Wolves"},
    {"name": "West Ham"},
    {"name": "Nottingham Forest"},
    {"name": "Sheffield United"},
    {"name": "Tottenham Hotspur"}
]

schema_squad_create_example = [
    {
        "player_id": 6
    },
    {
        "player_id": 10
    },
    {
        "player_id": 7
    },
    {
        "player_id": 5
    },
    {
        "player_id": 13
    },
    {
        "player_id": 22
    },
    {
        "player_id": 23
    },
    {
        "player_id": 2
    },
    {
        "player_id": 3
    },
    {
        "player_id": 4
    },
    {
        "player_id": 11
    },
    {
        "player_id": 17
    },
    {
        "player_id": 15
    },
    {
        "player_id": 19
    },
    {
        "player_id": 25
    }
]


def create_list_schema(club_list):
    club_create_schema_list = list(schemas.ClubCreate)
    for club in club_list:
        club_create_schema = schemas.ClubCreate(
            name=club
        )
        club_create_schema_list.append(club_create_schema)
