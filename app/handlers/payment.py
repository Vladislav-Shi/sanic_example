from sanic import Blueprint, json, Request, HTTPResponse
from sanic.exceptions import SanicException
from sanic_ext.extensions.openapi import openapi
from tortoise.transactions import in_transaction

from app.database import Transaction, Bill, TransactionStatus
from app.models import WebhookBody, WebhookResponse
from utis.hashing import get_signature

payment_bp = Blueprint('payment_blueprint', url_prefix='/payment')


@payment_bp.post('/webhook')
@openapi.definition(  # type: ignore[misc]
    body=WebhookBody,
)
async def change_balance(request: Request) -> HTTPResponse:
    payload = WebhookBody(**request.json)
    signature = get_signature(
        user_id=payload.user_id,
        transaction_id=payload.transaction_id,
        bill_id=payload.bill_id,
        amount=payload.amount
    )
    if signature != payload.signature:
        raise SanicException('Bad signature', status_code=400)
    transaction = await Transaction.get(pk=payload.transaction_id)
    bill = await Bill.get(pk=payload.bill_id)
    if bill.balance + payload.amount < 0:
        transaction.status = TransactionStatus.REJECTED
        await transaction.save()
    else:
        try:
            async with in_transaction():
                transaction.value = payload.amount
                transaction.after_balance = bill.balance + payload.amount
                transaction.status = TransactionStatus.COMPLETE
                bill.balance += payload.amount
                await bill.save()
                await transaction.save()
        except Exception:
            transaction.status = TransactionStatus.ERROR
            await transaction.save()
    response = WebhookResponse(result=transaction.status.value)
    return json(response.dict())
