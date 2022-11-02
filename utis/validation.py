from datetime import datetime, date
from enum import Enum
from json import dumps
from typing import Union, List, Sequence

from tortoise import Model

from config.setting import config


def true_check(value: str) -> bool:
    if value.lower() in ['true', 'True', '1', 'yes', 't', 'y']:
        return True
    else:
        return False


def get_url(server_path: str = '') -> str:
    """Генерирует ссылку по поти на сервере"""
    return f'{config.HOST}:{config.PORT}{server_path}'


def time_check(date_one: Union[int, datetime],
               date_two: Union[int, datetime]) -> bool:
    """Функция возвращает True если первое время больше второго"""
    if isinstance(date_one, datetime):
        date_one = int(date_one.strftime('%Y%m%d%H%M%S'))
    if isinstance(date_two, datetime):
        date_two = int(date_two.strftime('%Y%m%d%H%M%S'))
        print(date_one, date_two, date_one - date_two)
    if date_one - date_two > 0:
        return True
    return False


def json_dump(data: dict) -> str:
    """Обеспечивает работу с датами для функции Sanic.json
    Использование:
    json(body, dumps=json_dump)
    """

    def json_serial(obj: object) -> str:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value  # type: ignore
        raise TypeError(f'Type {type(obj)} not serializable')

    return dumps(data, default=json_serial)


async def objects_model_to_dict(
        objets: Union[Sequence[Model], Model],
        extract: List[str] = []
) -> Union[dict, list]:
    """Преобразует модель или набор моделей в словарь"""
    result: Union[List[dict], dict]
    if isinstance(objets, Model):
        result = dict(objets)
        for key in extract:
            if key in result:
                result.pop(key)
    elif isinstance(objets, list):
        result = []
        for product in objets:
            product_dict = dict(product)
            for key in extract:
                if key in product_dict:
                    product_dict.pop(key)
            result.append(product_dict)  # type: ignore[union-attr]
    else:
        raise ValueError('Object must be List[Model] or Model')
    return result
