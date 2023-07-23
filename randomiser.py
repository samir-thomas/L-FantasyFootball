import random


from faker import Faker

fake = Faker()


def assign_player_position():
    player_position = ["GKP", "DEF", "MID", "FWD"]

    random_position = random.choice(player_position)
    return random_position


def assign_player_club():
    clubs_options = ["Bournemouth",
                     "Arsenal",
                     "Aston Villa",
                     "Brentford",
                     "Brighton",
                     "Burnley",
                     "Chelsea",
                     "Crystal Palace",
                     "Everton",
                     "Fulham",
                     "Liverpool",
                     "Luton Town",
                     "Manchester City",
                     "Manchester United",
                     "Newcastle United"
                     ]
    random_club = random.choice(clubs_options)
    return random_club


def assign_points_total():
    return random.randint(20, 200)


def assign_cost():
    return round(random.uniform(1.0, 15.0), 1)


def assign_random_player_name():
    return fake.name()
