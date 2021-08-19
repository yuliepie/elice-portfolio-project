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


# Login a test user to test logout function
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


# Create fixture that adds users to database
@pytest.fixture(scope="module")
def add_users_to_db(test_client):
    data1 = {
        "email": "apple@testing.com",
        "password": "password123",
        "name": "김사과",
    }
    data2 = {
        "email": "banana@testing.com",
        "password": "password123",
        "name": "정바나나",
    }
    data3 = {
        "email": "cherry@testing.com",
        "password": "password123",
        "name": "이체리",
    }
    user1 = User(data1["email"], data1["password"], data1["name"])
    user1.description = "안녕하세요 사과입니다."

    user2 = User(data2["email"], data2["password"], data2["name"])
    user2.description = "안녕 나는 바나나."

    user3 = User(data3["email"], data3["password"], data3["name"])

    db.session.add_all([user1, user2, user3])
    db.session.commit()
    yield
