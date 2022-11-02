from datetime import datetime
from functools import wraps
from typing import Callable, Optional

import jwt
from sanic import text, Request
from sanic.log import logger

from app.database import User
from app.models import JwtPayload
from config.setting import config
from utis.validation import time_check


async def check_token(request: Request, role_check: bool = False) -> bool:
    """Также добавляет к запросу данные из токена и является ли юзер админом"""
    if not request.token:
        return False
    try:
        jwt_payload = JwtPayload(**jwt.decode(request.token, config.SECRET_KEY,
                                              algorithms=['HS256']))
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        if not time_check(jwt_payload.exp, datetime.utcnow()):
            logger.debug('time_check')
            return False
        user = await User.get_or_none(pk=jwt_payload.user_id)
        if user is None:
            logger.debug('user is None')
            return False
        if not user.is_active:
            logger.debug('user is not active')
            return False
        if role_check:
            if not user.is_admin:
                logger.debug('user is not admin')
                return False
        request.ctx.token_payload = jwt_payload
        request.ctx.is_admin = user.is_admin
        return True


def protected(  # type: ignore
        _func: Optional[Callable] = None,
        *,
        role_check: bool = False
) -> Callable:
    def _protected(wrapped: Callable):  # type: ignore
        def decorator(f: Callable):  # type: ignore
            @wraps(f)
            async def decorated_function(request, *args, **kwargs):  # type: ignore  # noqa
                is_authenticated = await check_token(request, role_check)

                if is_authenticated:
                    response = await f(request, *args, **kwargs)
                    return response
                else:
                    return text('You are unauthorized.', 401)

            return decorated_function

        return decorator(wrapped)

    if _func is None:
        return _protected
    else:
        return _protected(_func)
