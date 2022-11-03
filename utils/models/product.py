from typing import List

from sanic.exceptions import SanicException

from app.database import Product, Transaction, Bill, TransactionStatus
from app.models import ProductModel, UpdateProductModel


async def get_product_list(is_admin: bool = False) -> List[Product]:
    if is_admin:
        return await Product.all()
    return await Product.filter(is_active=True)


async def create_product(product_data: ProductModel) -> Product:
    return await Product.create(**product_data.dict())


async def get_product(product_pk: int, is_admin: bool = False) -> Product:
    product = await Product.get_or_none(pk=product_pk)
    if product is None:
        raise SanicException('product not found', status_code=400)
    if not is_admin and not product.is_active:
        raise SanicException('Access denied', status_code=407)
    return product


async def buy_product(product_id: int, user_id: int,
                      bill_id: int) -> Transaction:
    product = await get_product(product_pk=product_id)
    bill = await Bill.get_or_none(user__pk=user_id, pk=bill_id)
    if bill is None:
        raise SanicException('bill not found', status_code=400)
    if bill.balance < product.price:
        raise SanicException('Need more gold!!', status_code=400)
    transaction = await Transaction.create(
        bill=bill,
        value=-product.price,
        product=product,
        after_balance=bill.balance - product.price,
        status=TransactionStatus.COMPLETE
    )
    bill.balance -= product.price
    await bill.save()
    return transaction


async def delete_product(product_pk: int) -> None:
    product = await get_product(product_pk=product_pk)
    await product.delete()


async def update_product(product_pk: int,
                         update_field: UpdateProductModel) -> None:
    product = await get_product(product_pk=product_pk)
    await product.update_from_dict(data=update_field.dict(skip_defaults=True))
    await product.save()
