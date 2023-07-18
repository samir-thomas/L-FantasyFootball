from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse, Response, PlainTextResponse

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


def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}


templates = Jinja2Templates(
    directory='templates', context_processors=[app_context], autoescape=False, auto_reload=True)


async def homepage(request):
    context = {
        'request': request,
        "users": obj}
    return templates.TemplateResponse('index.jinja2', context)


async def get_all_users(request):
    context = {
        'request': request,
        "players": obj
    }
    return templates.TemplateResponse('users.jinja2', context)


async def get_user(request):
    user_id = request.path_params['id']
    context = {
        'request': request,
        "player_details": obj[user_id]
    }
    return templates.TemplateResponse('jungle.jinja2', context)


async def api_get_all_users(request):
    return JSONResponse(obj)


async def create_player(request):
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


routes = [
    Route('/', endpoint=homepage),
    Route('/users', get_all_users),
    Route('/users/{id:int}', get_user),
    Route('/api/users/all', api_get_all_users),
    Route('/api/users/new', create_player),
    Route('/api/users/edit/{id:int}', api_edit_player),
    Route('/api/users/remove/{id:int}', api_remove_user),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)
