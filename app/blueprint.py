from sanic import Sanic

from app.handlers.bill import bill_bp
from app.handlers.payment import payment_bp
from app.handlers.product import product_bp
from app.handlers.user import user_bp


def init_blueprint(app: Sanic) -> None:
    app.blueprint(user_bp)
    app.blueprint(product_bp)
    app.blueprint(payment_bp)
    app.blueprint(bill_bp)
