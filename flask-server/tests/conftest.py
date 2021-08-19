import pytest
from project import create_app
from flask import current_app
from project.models import User
from project import db

#####################################################
# Fixture that runs once per test module (file)
#####################################################

# Returns a test client from the testing app instance.
@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    flask_app.config.from_object("config.TestingConfig")

    # Create a test client using the Flask application configured for testing
    testing_client = flask_app.test_client()

    # Establish an application context
    ctx = flask_app.app_context()
    ctx.push()

    current_app.logger.info("Created test_client")
    db.create_all()  # Create SQLite Test DB

    yield testing_client

    db.drop_all()
    ctx.pop()  # Pop application context for cleanup


# Returns a new user from the User model.
@pytest.fixture(scope="module")
def new_user():
    user = User("test@testing.com", "password123", "김테스터")
    return user
