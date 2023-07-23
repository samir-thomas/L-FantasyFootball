from randomiser import *


def crate_player_database():
    data = []
    for num in range(100):
        player = {
            "name": assign_random_player_name(),
            "position": assign_player_position(),
            "club": assign_player_club(),
            "cost": assign_cost(),
            "total_points": assign_points_total(),
            "home_away": "H"
        }
        data.append(player)
    return data


