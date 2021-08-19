import pytest
from project import create_app
from flask import current_app, json
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


# Register a test user for login/logout
@pytest.fixture(scope="module")
def register_test_user(test_client):
    new_user_data = {
        "email": "testlogin@testing.com",
        "password": "password123",
        "name": "김로그인",
    }
    test_client.post(
        "/api/users", data=json.dumps(new_user_data), content_type="application/json"
    )
    yield


@pytest.fixture(scope="function")
def log_in_test_user(test_client, register_test_user):
    user_data = {
        "email": "testlogin@testing.com",
        "password": "password123",
    }
    test_client.post(
        "/api/login", data=json.dumps(user_data), content_type="application/json"
    )
    yield
    test_client.get("/api/logout")
