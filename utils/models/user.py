from datetime import datetime, timedelta
from typing import List

import jwt
from sanic import Sanic
from sanic.exceptions import SanicException

from app.database import User, Verification
from app.models import UserModel
from config.setting import config
from utils.hashing import get_password_hash, get_accept_string
from utils.validation import get_url


async def create_user(user_param: UserModel) -> User:
    try:
        return await User.create(
            username=user_param.username,
            password=get_password_hash(password=user_param.password)
        )
    except Exception:
        raise SanicException('user already exists', status_code=400)


async def create_superuser(username: str, password: str) -> None:
    await User.get_or_create(
        username=username,
        password=get_password_hash(password=password),
        is_active=True,
        is_admin=True
    )


async def user_login(user_param: UserModel) -> str:
    user = await User.get_or_none(
        username=user_param.username,
        password=get_password_hash(password=user_param.password)
    )
    if user is None:
        raise SanicException('user not found', status_code=400)
    if user.is_active:
        payload = {
            'user_id': user.pk,
            'exp': (datetime.utcnow() + timedelta(
                seconds=config.TOKEN_TTL)).strftime('%Y%m%d%H%M%S')
        }
        token = jwt.encode(payload=payload, key=config.SECRET_KEY, algorithm='HS256')
        return token
    raise SanicException('user not activated', status_code=400)


async def create_accept_url(user: User) -> str:
    app = Sanic.get_app(name=config.APP_NAME)
    url_key = get_accept_string(username=user.username, pk=user.pk)
    await Verification.create(user=user, link=url_key)
    return get_url(
        app.url_for(view_name='user_blueprint.accept_user_link', url=url_key))


async def accept_user(url_postfix: str) -> None:
    link = await Verification.get_or_none(link=url_postfix)
    if link is None:
        raise SanicException('link not found', status_code=400)
    user = await link.user
    await link.delete()
    if user.is_active:
        raise SanicException('user has been activated', status_code=400)
    user.is_active = True
    await user.save()


async def change_user_status(user_id: int, active: bool) -> None:
    user = await User.get_or_none(pk=user_id)
    if user is None:
        raise SanicException('User not found', 400)
    user.is_active = active
    await user.save()


async def get_user_list() -> List[User]:
    return await User.all()
