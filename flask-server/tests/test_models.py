from flask_bcrypt import generate_password_hash
from project.models import User
from project import bcrypt

"""
Tests for models.py
"""


def test_new_user(new_user):
    """
    GIVEN a user model,
    WHEN a new user object is created,
    THEN check the email, hashed password and name is correct.
    """
    assert new_user.email == "test@testing.com"
    assert new_user.password_hashed != "password123"
    assert new_user.name == "김테스터"
