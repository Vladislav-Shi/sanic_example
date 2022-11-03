from typing import List

from sanic import Blueprint, json, Request, HTTPResponse
from sanic.exceptions import SanicException
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.definitions import Response, Parameter

import utils.models.product as p
from app.models import ProductModel, FullProductModel, UpdateProductModel, BaseResponse, StatusCode, BaseResponseBody
from utils.auth import protected
from utils.validation import json_dump, objects_model_to_dict

product_bp = Blueprint('product_blueprint', url_prefix='/product')


@product_bp.get('/list')
@openapi.definition(  # type: ignore
    response=[Response(List[FullProductModel])],
    secured='token')  # type: ignore[arg-type]
@protected
async def product_list(request: Request) -> HTTPResponse:
    products = await p.get_product_list(is_admin=request.ctx.is_admin)
    response = BaseResponse(
        payload=await objects_model_to_dict(products, extract=['update_at']),
        status_code=StatusCode.OK
    )
    return json(response.payload, dumps=json_dump, status=response.status_code.value)


@product_bp.get('/<product_id:int>')
@openapi.definition(  # type: ignore
    response=[Response(FullProductModel)],
    secured='token')  # type: ignore[arg-type]
@protected
async def product_info(request: Request, product_id: int) -> HTTPResponse:
    products = await p.get_product(
        product_pk=product_id,
        is_admin=request.ctx.is_admin
    )
    response = BaseResponse(
        payload=await objects_model_to_dict(products),
        status_code=StatusCode.OK
    )
    return json(response.payload, dumps=json_dump, status=response.status_code.value)


@product_bp.post('/<product_id:int>/buy')
@openapi.definition(  # type: ignore
    parameter=[Parameter('bill', schema=int, required=True)],
    secured='token')  # type: ignore[arg-type]
@protected
async def buy_product(request: Request, product_id: int) -> HTTPResponse:
    try:
        bill_id = int(request.args.get('bill', default=None))
    except Exception:
        raise SanicException('enter correct bill', status_code=StatusCode.BAD_REQUEST.value)

    transaction = await p.buy_product(
        product_id=product_id,
        bill_id=bill_id,
        user_id=request.ctx.token_payload.user_id
    )
    response = BaseResponse(
        payload=await objects_model_to_dict(transaction),
        status_code=StatusCode.OK
    )
    return json(response.payload, dumps=json_dump, status=response.status_code.value)


@product_bp.post('/')
@openapi.definition(  # type: ignore
    body=ProductModel,
    secured='token')  # type: ignore[arg-type]
@protected(role_check=True)
async def create_product(request: Request) -> HTTPResponse:
    product = await p.create_product(product_data=ProductModel(**request.json))
    response = BaseResponse(
        payload=BaseResponseBody(message=product.pk).dict(),
        status_code=StatusCode.CREATED
    )
    return json(response.payload, dumps=json_dump, status=response.status_code.value)


@product_bp.put('/<product_id:int>')
@openapi.definition(  # type: ignore[misc]
    body=UpdateProductModel,
    secured='token')  # type: ignore[arg-type]
@protected(role_check=True)
async def change_product(request: Request, product_id: int) -> HTTPResponse:
    await p.update_product(
        product_pk=product_id,
        update_field=UpdateProductModel(**request.json)
    )
    response = BaseResponse(
        payload=BaseResponseBody(message='OK').dict(),
        status_code=StatusCode.OK
    )
    return json(response.payload, dumps=json_dump, status=response.status_code.value)


@product_bp.delete('/<product_id:int>')
@openapi.definition(  # type: ignore[misc]
    secured='token')  # type: ignore[arg-type]
@protected(role_check=True)
async def delete_product(request: Request, product_id: int) -> HTTPResponse:
    await p.delete_product(product_pk=product_id)
    response = BaseResponse(
        payload=BaseResponseBody(message='OK').dict(),
        status_code=StatusCode.OK
    )
    return json(response.payload, dumps=json_dump, status=response.status_code.value)
