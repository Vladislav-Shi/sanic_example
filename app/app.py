from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise

from app.blueprint import init_blueprint
from config.setting import TORTOISE_CONFIG, config
from utils.models.user import create_superuser


def init_app() -> Sanic:
    app = Sanic(name=config.APP_NAME)
    init_blueprint(app)
    register_tortoise(app=app, config=TORTOISE_CONFIG, generate_schemas=False)
    app.ext.openapi.add_security_scheme(
        'token',
        'http',
        scheme='bearer',
        bearer_format='JWT',
    )

    # создание админа если его нет
    @app.listener('before_server_start')  # type: ignore[arg-type]
    async def pre_add(app: Sanic, loop: str) -> None:
        await create_superuser(
            username=config.ADMIN_NAME,
            password=config.ADMIN_PASS
        )

    return app
