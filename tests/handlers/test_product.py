import asyncio
from datetime import datetime, timedelta
from unittest.mock import patch, AsyncMock, Mock

import jwt
import pytest
from sanic import Sanic


from config.setting import config
from tests.helpers.database import create_product, to_response_view


async def create_products():
    product_1 = create_product()
    await product_1.save()
    product_2 = create_product(pk=2, heading='heading_2', is_active=False)
    await product_2.save()
    return [product_1, product_2]


class TestProduct:

    @pytest.mark.asyncio
    @patch('utils.models.product.get_product_list', Mock(return_value=create_products()))
    async def test_get_product_list(self, app: Sanic, database):
        products = await create_products()

        payload = {
            'user_id': 1,  # id админа
            'exp': (datetime.utcnow() + timedelta(
                seconds=config.TOKEN_TTL)).strftime('%Y%m%d%H%M%S')
        }
        headers = {'Authorization': jwt.encode(payload=payload, key=config.SECRET_KEY, algorithm='HS256')}

        request, response = await app.asgi_client.get(app.url_for('product_blueprint.product_list'), headers=headers)

        assert request.method.lower() == "get"
        assert response.json == await to_response_view(products, extract=['update_at'])
        assert response.status == 200

    @pytest.mark.asyncio
    @patch('utils.models.product.get_product_list', Mock(return_value=create_products()))
    async def test_get_product_list_for_basic_user(self, app: Sanic, database):
        products = await create_products()

        payload = {
            'user_id': 2,  # id обычного
            'exp': (datetime.utcnow() + timedelta(
                seconds=config.TOKEN_TTL)).strftime('%Y%m%d%H%M%S')
        }
        headers = {'Authorization': jwt.encode(payload=payload, key=config.SECRET_KEY, algorithm='HS256')}

        request, response = await app.asgi_client.get(app.url_for('product_blueprint.product_list'), headers=headers)

        assert request.method.lower() == "get"
        assert response.status == 200
        assert response.json == await to_response_view(products, extract=['update_at'])







