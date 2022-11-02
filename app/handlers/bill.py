from typing import List

import aiohttp
from sanic import Blueprint, json, Request, HTTPResponse
from sanic.exceptions import SanicException
from sanic_ext.extensions.openapi import openapi
from sanic_ext.extensions.openapi.definitions import Response, Parameter

import utis.models.bill as b
from app.models import BillModel, WebhookResponse
from utis.auth import protected
from utis.validation import json_dump, objects_model_to_dict

bill_bp = Blueprint('bill_blueprint', url_prefix='/bill')


@bill_bp.get('/')
@openapi.definition(  # type: ignore[misc]
    response=[Response(List[BillModel])],
    secured='token')  # type: ignore[arg-type]
@protected
async def get_bills(request: Request) -> HTTPResponse:
    bills = await b.get_bills(user_id=request.ctx.token_payload.user_id)
    bills_dict = await objects_model_to_dict(bills)
    return json(bills_dict, dumps=json_dump)


@bill_bp.get('/history')
@openapi.definition(  # type: ignore[misc]
    parameter=[Parameter('bill', schema=int, required=True)],
    secured='token')  # type: ignore[arg-type]
@protected
async def get_history(request: Request) -> HTTPResponse:
    try:
        bill_id = int(request.args.get('bill', default=None))
    except Exception:
        raise SanicException('enter correct bill', status_code=400)

    transactions = await b.get_bill_history(
        bill_id=bill_id,
        user_id=request.ctx.token_payload.user_id
    )
    transactions_dict = await objects_model_to_dict(transactions)
    return json(transactions_dict, dumps=json_dump)


@bill_bp.post('/add')
@openapi.definition(  # type: ignore[misc]
    parameter=[
        Parameter('bill', schema=int, required=False),
        Parameter('balance', schema=int, required=True)
    ],
    secured='token')  # type: ignore[arg-type]
@protected
async def add_balance(request: Request) -> HTTPResponse:
    try:
        balance = int(request.args.get('balance', default=None))
    except Exception:
        raise SanicException('enter correct balance', status_code=400)

    webhook_params = await b.add_balance_response(
        bill_id=request.args.get('bill', default=None),
        user_id=request.ctx.token_payload.user_id,
        balance=balance
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(url=webhook_params.url,
                                json=webhook_params.payload.dict()) as resp:
            resp_body = await resp.json()
            resp_body = WebhookResponse(**resp_body)
    return json({
        'message': f'bill with id={webhook_params.payload.bill_id} complite with status {resp_body.result}'})  # noqa


@bill_bp.get('/all')
@openapi.definition(  # type: ignore[misc]
    secured='token')  # type: ignore[arg-type]
@protected(role_check=True)
async def all_users_bills(request: Request) -> HTTPResponse:
    bills = await b.get_all_users_bill()
    bills_dict = await objects_model_to_dict(bills)
    return json(bills_dict, dumps=json_dump)
