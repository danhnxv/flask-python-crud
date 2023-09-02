import pytest
from app import app, db


@pytest.fixture
def init_app():
    app.config.from_object("app.config.TestingConfig")
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture
def client(init_app):
    return init_app.test_client()


@pytest.fixture(scope="module")
def database():
    app.config.from_object("app.config.TestingConfig")
    db.create_all()

    yield db
    db.session.remove()
    db.drop_all()
