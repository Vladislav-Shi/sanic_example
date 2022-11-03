import json
from datetime import datetime
from typing import Union, Sequence, List

from tortoise import Model

from app.database import Product, User
from utils.hashing import get_password_hash
from utils.validation import json_dump, objects_model_to_dict


def create_date() -> datetime:
    return datetime(year=2022, day=1, month=1, second=1, microsecond=1, minute=1, hour=1)


def create_product(
        pk: int = 1,
        heading: str = 'heading',
        description: str = 'description',
        price: int = 100,
        is_active: bool = True,
        create_at: datetime = create_date(),
        update_at: datetime = create_date()
) -> Product:
    return Product(
        pk=pk,
        description=description,
        heading=heading,
        price=price,
        is_active=is_active,
        create_at=create_at,
        update_at=update_at
    )


def create_user(
        pk: int = 1,
        username: str = 'test',
        is_admin: bool = True,
        password: str = 'test',
        create_at: datetime = create_date(),
        update_at: datetime = create_date()
) -> User:
    return User(
        pk=pk,
        username=username,
        is_admin=is_admin,
        password=get_password_hash(password),
        create_at=create_at,
        update_at=update_at
    )


async def to_response_view(
        objets: Union[Sequence[Model], Model],
        extract: List[str] = []
) -> dict:
    result = json_dump(await objects_model_to_dict(objets=objets, extract=extract))
    return json.loads(result)
