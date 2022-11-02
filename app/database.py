from enum import Enum

from tortoise import Model, fields


class TransactionStatus(Enum):
    IN_PROCESS = 'process'
    COMPLETE = 'complete'
    REJECTED = 'rejected'
    ERROR = 'error'


class User(Model):
    username = fields.CharField(max_length=32, unique=True)
    is_admin = fields.BooleanField(default=False)
    # TODO Добавить валидаторы
    is_active = fields.BooleanField(default=False)
    password = fields.CharField(max_length=256)
    create_at = fields.DatetimeField(auto_now_add=True, index=True)
    update_at = fields.DatetimeField(auto_now=True)


class Verification(Model):
    user = fields.ForeignKeyField('models.User')  # type: ignore
    link = fields.CharField(max_length=256)
    create_at = fields.DatetimeField(auto_now_add=True)


class Product(Model):
    heading = fields.CharField(max_length=256, unique=True)
    description = fields.TextField(null=True)
    # TODO Добавить валидаторы
    price = fields.IntField()
    is_active = fields.BooleanField(default=True)
    create_at = fields.DatetimeField(auto_now_add=True, index=True)
    update_at = fields.DatetimeField(auto_now=True)


class Bill(Model):
    balance = fields.IntField(default=0)
    user = fields.ForeignKeyField('models.User')  # type: ignore
    create_at = fields.DatetimeField(auto_now_add=True, index=True)
    update_at = fields.DatetimeField(auto_now=True)


class Transaction(Model):
    bill = fields.ForeignKeyField('models.Bill')  # type: ignore
    value = fields.IntField(null=True)
    product = fields.ForeignKeyField('models.Product', null=True)  # type: ignore  # noqa
    after_balance = fields.IntField(null=True)
    create_at = fields.DatetimeField(auto_now_add=True, index=True)
    status = fields.CharEnumField(
        enum_type=TransactionStatus,
        max_length=32,
        default=TransactionStatus.IN_PROCESS
    )
