from Crypto.Hash import SHA256  # type: ignore[import]

from config.setting import config


def get_signature(
        transaction_id: int,
        user_id: int, bill_id: int,
        amount: int
) -> str:
    h = SHA256.new()
    h.update(
        f'{config.SECRET_KEY}:{transaction_id}:{user_id}:{bill_id}:{amount}'.encode())  # noqa
    return h.hexdigest()


def get_password_hash(password: str) -> str:
    h = SHA256.new()
    h.update(f'{config.SECRET_KEY}:{password}'.encode())
    return h.hexdigest()


def get_accept_string(username: str, pk: int) -> str:
    h = SHA256.new()
    h.update(f'{config.SECRET_KEY}:{username}:{pk}'.encode())
    return h.hexdigest()
