from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StatusCode(Enum):
    OK: 200
    CREATED: 201

    MOVE_PERMANENT: 301
    MOVE_TEMP: 302

    BAD_REQUEST: 400
    UNAUTHORIZED: 401
    FORBIDDEN: 403
    NOT_FOUND: 404

    INTERNAL_ERROR: 500
    NOT_IMPLEMENTED: 501


class UserModel(BaseModel):
    username: str
    password: str


class VerifyUrlResponse(BaseModel):
    verify_url: str


class WebhookBody(BaseModel):
    signature: str
    transaction_id: int
    user_id: int
    bill_id: int
    amount: int


class WebhookRequestModel(BaseModel):
    url: str
    payload: WebhookBody


class JwtPayload(BaseModel):
    user_id: int
    exp: int


class ProductModel(BaseModel):
    pk: Optional[int]
    heading: str
    description: Optional[str]
    price: int


class FullProductModel(ProductModel):
    is_active: bool
    create_at: str
    update_at: str


class UpdateProductModel(BaseModel):
    pk: Optional[int]
    heading: Optional[str]
    description: Optional[str]
    price: Optional[int]
    is_active: Optional[bool]
    create_at: Optional[str]
    update_at: Optional[str]


class BillModel(BaseModel):
    id: int
    balance: int


class BaseResponseBody(BaseModel):
    message: str


class BaseResponse(BaseModel):
    status_code: StatusCode
    payload: dict
