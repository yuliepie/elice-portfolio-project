from datetime import date
import pytest
from project import create_app
from flask import current_app, json
from project.models import (
    User,
    EducationStatus,
    Education,
    Award,
    Project,
    Certification,
)
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

    # seed education status
    status1 = EducationStatus("재학중")
    status2 = EducationStatus("학사졸업")
    status3 = EducationStatus("석사졸업")
    status4 = EducationStatus("박사졸업")
    db.session.add_all([status1, status2, status3, status4])
    db.session.commit()

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


# Create fixture that adds users to test database
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


# Create fixture that adds user details to test database
@pytest.fixture(scope="module")
def add_user_details(test_client, register_test_user):
    data_raw = {
        "edu1": ["학교1", "전공1", 1, 1],
        "edu2": ["학교2", "전공2", 2, 1],
        "award1": ["수상1", "수상내역", 1],
        "award2": ["수상2", "수상내역", 1],
        "proj1": ["프로젝트1", "프로젝트내역", date(2020, 1, 1), date(2020, 2, 2), 1],
        "proj2": ["프로젝트2", "프로젝트내역", date(2021, 1, 1), date(2021, 2, 2), 1],
        "cert1": ["자격증1", "발급자", date(2020, 1, 1), 1],
        "cert2": ["자격증2", "발급자", date(2021, 2, 2), 1],
    }

    edu1 = Education(*data_raw["edu1"])
    edu2 = Education(*data_raw["edu2"])
    aw1 = Award(*data_raw["award1"])
    aw2 = Award(*data_raw["award2"])
    proj1 = Project(*data_raw["proj1"])
    proj2 = Project(*data_raw["proj2"])
    cert1 = Certification(*data_raw["cert1"])
    cert2 = Certification(*data_raw["cert2"])

    db.session.add_all([edu1, edu2, aw1, aw2, proj1, proj2, cert1, cert2])
    db.session.commit()
    yield data_raw
