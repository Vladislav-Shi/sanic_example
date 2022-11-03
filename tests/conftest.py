from typing import Generator

import pytest
from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise
from tortoise.contrib.test import initializer, finalizer, _restore_default

from app.blueprint import init_blueprint
from config.setting import config
from tests.helpers.database import create_user

from utils.models.user import create_superuser


def test_app() -> Sanic:
    app = Sanic(name=config.APP_NAME)
    init_blueprint(app)
    register_tortoise(
        app=app,
        db_url='sqlite://:memory:',
        modules={'models': ['app.database']},
        generate_schemas=True
    )

    @app.listener('before_server_start')  # type: ignore[arg-type]
    async def pre_add(app: Sanic, loop: str) -> None:
        await create_superuser(
            username=config.ADMIN_NAME,
            password=config.ADMIN_PASS
        )
        user = create_user()
        await user.save()

    app.ext.openapi.add_security_scheme(
        'token',
        'http',
        scheme='bearer',
        bearer_format='JWT',
    )
    return app


@pytest.fixture
def app():
    sanic_app = test_app()
    return sanic_app


@pytest.fixture()
def database() -> Generator:
    initializer(['app.database'])
    _restore_default()
    try:
        yield
    finally:
        finalizer()
