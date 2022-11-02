from sanic import Blueprint, json, HTTPResponse
from sanic.request import Request
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.definitions import Response, Parameter

import utis.models.user as u
from app.models import UserModel, VerifyUrlResponse
from utis.auth import protected
from utis.validation import objects_model_to_dict, json_dump, true_check

user_bp = Blueprint('user_blueprint', url_prefix='/user')


@user_bp.post('/signup')
@openapi.definition(  # type: ignore[misc]
    body=UserModel,
    response=[
        Response(VerifyUrlResponse, status=200),
        Response('error message', status=400)
    ],
)
async def sing_up(request: Request) -> HTTPResponse:
    user_param = UserModel(**request.json)
    user = await u.create_user(user_param=user_param)
    link = await u.create_accept_url(user=user)
    return json({'message': link})


@user_bp.get('/accept/<url:str>')
async def accept_user_link(request: Request, url: str) -> HTTPResponse:
    await u.accept_user(url_postfix=url)
    return json({'message': 'OK'})


@user_bp.post('/signin')
@openapi.definition(  # type: ignore[misc]
    body=UserModel,
    response=[
        Response(VerifyUrlResponse, status=200),
        Response({'detail': 'fail'}, status=400)
    ],
)
async def sing_in(request: Request) -> HTTPResponse:
    user_param = UserModel(**request.json)
    token = await u.user_login(user_param)
    return json({'token': token})


@user_bp.put('/<user_id:int>')
@openapi.definition(  # type: ignore[misc]
    parameter=[Parameter('active', schema=bool, required=True)],
    secured='token'  # type: ignore
)
@protected(role_check=True)
async def change_user(request: Request, user_id: int) -> HTTPResponse:
    active: str = request.args.get('active')
    await u.change_user_status(user_id=user_id, active=true_check(active))
    return json({'message': 'OK'})


@user_bp.get('/list')
@openapi.definition(  # type: ignore[misc]
    secured='token'  # type: ignore
)
@protected(role_check=True)
async def get_user_list(request: Request) -> HTTPResponse:
    users = await u.get_user_list()
    users_dict = await objects_model_to_dict(users, extract=['password'])
    return json(users_dict, dumps=json_dump)
