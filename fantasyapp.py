from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse, Response, PlainTextResponse
from players import crate_player_database


import typing

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
            "Foder",
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


async def homepage(request):
    context = {
        'request': request,
        "users": obj}
    return templates.TemplateResponse('homepage.jinja2', context)


async def get_all_users(request):
    context = {
        'request': request,
        "registered_users": obj
    }
    return templates.TemplateResponse('users.jinja2', context)


async def get_user_details_page(request):
    user_id = request.path_params['id']
    context = {
        'request': request,
        "player_details": obj[user_id]
    }
    return templates.TemplateResponse('user_details.jinja2', context)


async def api_get_all_users(request):
    return JSONResponse(obj)


async def api_create_player(request):
    player = {
        "first_name": "new_firstname",
        "surname": "new_surname",
        "email": "new_player@email.com",
        "username": "new_player_username"
    }
    obj.append(player)
    return JSONResponse(obj)


async def api_edit_player(request):
    user_id = request.path_params['id']
    obj[user_id] = {
        "first_name": "edited_firstname",
        "surname": "edited_surname",
        "email": "edited_player@email.com",
        "username": "edited_player_username"
    }
    return JSONResponse(obj)


async def api_remove_user(request):
    user_id = request.path_params['id']
    obj.remove(obj[user_id])
    return JSONResponse(obj)


async def api_get_squad(request):
    return JSONResponse(my_fp_squad)


async def api_get_player_details(request):
    return JSONResponse(crate_player_database())


def welcome_page(request):
    user_id = request.path_params['id']
    context = {
        'request': request,
        'player_details': obj[user_id],
        'squad': [my_squad for my_squad
                  in my_fp_squad if my_squad.get("owner") == obj[user_id].get("username")]
    }
    return templates.TemplateResponse('welcome.jinja2', context)


def get_players_db(request):
    context = {
        'request': request,
        'players_list': crate_player_database()
    }
    return templates.TemplateResponse('players_list_table.jinja2', context)


routes = [
    Route('/', endpoint=homepage),
    Route('/welcome/{id:int}', welcome_page),
    Route('/users', get_all_users),
    Route('/users/{id:int}', get_user_details_page),
    Route('/players_database', get_players_db),
    Route('/api/users/all', api_get_all_users),
    Route('/api/users/new', api_create_player),
    Route('/api/users/edit/{id:int}', api_edit_player),
    Route('/api/users/remove/{id:int}', api_remove_user),
    Route('/api/squads', api_get_squad),
    Route('/api/players_list', api_get_player_details),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)
