from players import crate_player_database
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import typing

app = FastAPI()

obj = [
    {
        "first_name": "Samir",
        "surname": "Thomas",
        "email": "john_doe@email.com",
        "username": "testproject"},
    {
        "first_name": "Player 2_first",
        "surname": "Player 2_surname",
        "email": "john_doe2@email.com",
        "username": "testproject2"},
]

my_fp_squad = [
    {
        "owner": "testproject2",
        "Goalkeepers": {
            "Raya",
            "Pope",
        },
        "Defenders": {
            "Trippier",
            "Perisic",
            "Dier",
            "Henry",
            "Robertson",
        },
        "Midfielders": {
            "Andreas",
            "Iwobi",
            "Maddison",
            "Mac Allister",
            "Foden",
        },
        "Forwards": {
            "Watkins",
            "Isak",
            "Mitrovic"
        }
    }
]


def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


templates = Jinja2Templates(
    directory='templates', context_processors=[app_context], autoescape=False, auto_reload=True)


@app.get("/")
async def homepage(request: Request):
    context = {
        'request': request,
        "users": obj}
    return templates.TemplateResponse('homepage.jinja2', context)


@app.get("/users")
async def get_all_users(request: Request):
    context = {
        'request': request,
        "registered_users": obj
    }
    return templates.TemplateResponse('users.jinja2', context)


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user_details_page(request: Request, user_id: int):
    context = {
        'request': request,
        "player_details": obj[user_id]
    }
    return templates.TemplateResponse('user_details.jinja2', context)


@app.get("/welcome_page/{player_id}", response_class=HTMLResponse)
def welcome_page(request: Request, player_id: int):
    # user_id = request.path_params['id']
    context = {
        'request': request,
        'player_details': obj[player_id],
        'squad': [my_squad for my_squad
                  in my_fp_squad if my_squad.get("owner") == obj[player_id].get("username")]
    }
    return templates.TemplateResponse('welcome.jinja2', context)


@app.get("/api/users/all")
async def api_get_all_users():
    return obj


@app.get("/api/users/new")
async def api_create_player():
    player = {
        "first_name": "new_firstname",
        "surname": "new_surname",
        "email": "new_player@email.com",
        "username": "new_player_username"
    }
    obj.append(player)
    return obj


@app.get("/api/users/edit/{user_id}")
async def api_edit_player(user_id: int):
    obj[user_id] = {
        "first_name": "edited_firstname",
        "surname": "edited_surname",
        "email": "edited_player@email.com",
        "username": "edited_player_username"
    }
    return obj


@app.get("/api/users/remove/{user_id}")
async def api_remove_user(user_id: int):
    obj.remove(obj[user_id])
    return obj


@app.get("/api/squads")
async def api_get_squad():
    return my_fp_squad


@app.get("/api/players_list")
async def api_get_player_details():
    return crate_player_database()


@app.get("/players_database")
def get_players_db(request: Request):
    context = {
        'request': request,
        'players_list': crate_player_database()
    }
    return templates.TemplateResponse('players_list_table.jinja2', context)
