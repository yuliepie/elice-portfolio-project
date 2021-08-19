from project import create_app
from flask import json

"""
test_client is created by a fixture before the tests run,
and passed into each test.
"""


def test_test(test_client):
    response = test_client.get("/api/")
    print("aaaa", response.headers.get("Location"))
    print(response)
    assert response.status_code == 200


def test_register_user(test_client):
    """
    GIVEN a Flask app,
    WHEN valid data is posted to '/users' (POST)
    THEN check the response is success and user is registered.
    """
    new_user_data = {
        "email": "test@testing.com",
        "password": "password123",
        "name": "김테스터",
    }
    response = test_client.post(
        "/api/users", data=json.dumps(new_user_data), content_type="application/json"
    )
    response_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response_data["result"] == 1
    assert response_data["message"] == "registration success"


def test_invalid_register(test_client):
    """
    GIVEN a Flask app for testing,
    WHEN invalid data is posted to '/users' with missing password (POST)
    THEN check the response is failure.
    """
    new_user_data = {"email": "test2@testing.com", "name": "김테스터2"}
    response = test_client.post(
        "/api/users", data=json.dumps(new_user_data), content_type="application/json"
    )
    response_data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response_data["result"] == 0
    assert response_data["message"] == "registration fail"


def test_duplicate_user(test_client):
    """
    GIVEN a Flask app for testing,
    WHEN invalid data is posted to '/users' with existing email (POST)
    THEN check the response is fail - exiting user.
    """
    new_user_data1 = {"email": "test3@testing.com", "name": "김테스터", "password": "123"}
    new_user_data2 = {"email": "test3@testing.com", "name": "김테스터", "password": "123"}
    test_client.post(
        "/api/users", data=json.dumps(new_user_data1), content_type="application/json"
    )
    response = test_client.post(
        "/api/users", data=json.dumps(new_user_data2), content_type="application/json"
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 0
    assert response_data["message"] == "existing user"


def test_valid_login_and_logout(test_client, register_test_user):
    """
    GIVEN a Flask app for testing,
    WHEN valid credential data is posted to '/login' (POST)
    THEN check response is success.
    """
    login_data = {
        "email": "testlogin@testing.com",
        "password": "password123",
    }
    response = test_client.post(
        "/api/login", data=json.dumps(login_data), content_type="application/json"
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 1

    """
    WHEN request to '/logout' is made for logged in user (GET)
    THEN check response is success.
    """
    response = test_client.get("/api/logout")
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 1


def test_invalid_login(test_client, register_test_user):
    """
    GIVEN a flask app for testing,
    WHEN invalid credentials are posted to '/login' (POST)
    THEN check response is fail.
    """
    login_data = {
        "email": "testlogin@testing.com",
        "password": "password123wrong",
    }
    response = test_client.post(
        "/api/login", data=json.dumps(login_data), content_type="application/json"
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 0


def test_error_login_when_already_loggedin(test_client, log_in_test_user):
    """
    GIVEN a flask app for testing,
    WHEN credentials are posted to '/login' when user is already logged in (POST)
    THEN check response is fail.
    """
    login_data = {
        "email": "testlogin@testing.com",
        "password": "password123",
    }
    response = test_client.post(
        "/api/login", data=json.dumps(login_data), content_type="application/json"
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 0


def test_error_logout_when_not_loggedin(test_client):
    """
    GIVEN a flask app for testing,
    WHEN a request is made to '/logout' when user not logged in (GET)
    THEN check response is fail.
    """

    test_client.get("/api/logout")  # Log out just in case
    response = test_client.get("/api/logout")

    assert response.status_code == 401


def test_view_all_users_list(test_client, add_users_to_db):
    """
    GIVEN a flask app for testing,
    WHEN a request is made to '/users' (GET)
    THEN check response contains list of user data (id, name, description)
    """

    response = test_client.get("/api/users")
    response_data = json.loads(response.get_data(as_text=True))
    users_data = response_data["users"]

    assert response.status_code == 200
    assert response_data["result"] == 1
    assert any(
        user["name"] == "김사과" and user["description"] == "안녕하세요 사과입니다."
        for user in users_data
    )
    assert any(
        user["name"] == "정바나나" and user["description"] == "안녕 나는 바나나."
        for user in users_data
    )
    assert any(
        user["name"] == "이체리" and user["description"] == None for user in users_data
    )


def test_view_users_list_by_search(test_client, add_users_to_db):
    """
    GIVEN a flask app for testing,
    WHEN a requst is made to '/users?name=someName' (GET)
    THEN check response contains list of users matching query string
    """
    response = test_client.get("/api/users?name=김사")
    response_data = json.loads(response.get_data(as_text=True))
    users_data = response_data["users"]

    assert response.status_code == 200
    assert response_data["result"] == 1
    assert len(users_data) == 1
    assert users_data[0].get("name") == "김사과"
