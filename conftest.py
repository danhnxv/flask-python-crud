# Import necessary modules and packages
import pytest
from app import app, db


# Fixture to initialize the Flask application
@pytest.fixture(scope="session")
def init_app():
    # Context manager to ensure the app is in the application context
    with app.app_context():
        yield app


# Fixture to provide a test client for the initialized app
@pytest.fixture
def client(init_app):
    return init_app.test_client()


# Fixture to initialize the database for testing
@pytest.fixture(scope="session")
def database(init_app):
    # Context manager to ensure the app and database are in the application context
    with init_app.app_context():
        # Create all tables in the database
        db.create_all()

        yield db  # Provide the database instance to the test cases

        # Remove the session and drop all tables after tests
        db.session.remove()
        db.drop_all()
