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
