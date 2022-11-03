from typing import Generator

import pytest
from tortoise.contrib.test import initializer, finalizer, _restore_default

from app.app import test_app


@pytest.fixture
def app():
    sanic_app = test_app()
    return sanic_app


@pytest.fixture()
def database() -> Generator:
    initializer(['app.database'])
    _restore_default()
    try:
        yield
    finally:
        finalizer()
