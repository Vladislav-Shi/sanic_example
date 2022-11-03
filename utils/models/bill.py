from typing import List, Optional

from sanic import Sanic
from sanic.exceptions import SanicException

from app.database import Bill, Transaction, User
from app.models import WebhookBody, WebhookRequestModel
from config.setting import config
from utils.hashing import get_signature
from utils.validation import get_url


async def get_bills(user_id: int) -> List[Bill]:
    return await Bill.filter(user__pk=user_id)


async def get_bill_history(bill_id: int, user_id: int) -> List[Transaction]:
    return await Transaction.filter(bill__pk=bill_id, bill__user__pk=user_id)


async def add_balance_response(
        balance: int,
        user_id: int,
        bill_id: Optional[int] = None
) -> WebhookRequestModel:
    if balance <= 0:
        raise SanicException('adding balance must be greater than zero',
                             status_code=400)
    user = await User.get_or_none(pk=user_id)  # type: ignore[assignment]
    if user is None:
        raise SanicException('User not found')
    if bill_id is None:
        bill = await Bill.create(user=user)
    else:
        bill = await Bill.get_or_none(user=user, pk=bill_id)  # type: ignore
        if bill is None:
            raise SanicException('bill not found', status_code=404)
    transaction = await Transaction.create(bill=bill)
    app = Sanic.get_app(name=config.APP_NAME)
    url = get_url(app.url_for(view_name='payment_blueprint.change_balance'))
    signature = get_signature(user_id=user_id, transaction_id=transaction.pk,
                              bill_id=bill.pk, amount=balance)
    payload = WebhookBody(
        signature=signature,
        transaction_id=transaction.pk,
        user_id=user_id,
        bill_id=bill.pk,
        amount=balance
    )
    return WebhookRequestModel(url=url, payload=payload)


async def get_all_users_bill() -> List[Bill]:
    bills = await Bill.all().prefetch_related('user')
    return bills
