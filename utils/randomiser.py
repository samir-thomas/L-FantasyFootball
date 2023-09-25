import random


from faker import Faker


fake = Faker()


def assign_player_position():
    player_position = ["GKP", "DEF", "MID", "FWD"]

    random_position = random.choice(player_position)
    return random_position


def assign_points_total():
    return random.randint(20, 200)


def assign_cost():
    return round(random.uniform(1.0, 15.0), 1)


def assign_random_player_name():
    return fake.name()



