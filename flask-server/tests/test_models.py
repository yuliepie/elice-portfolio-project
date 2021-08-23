from flask_bcrypt import generate_password_hash
from project.models import User, Education, Award, Project, Certification
from project import bcrypt
from datetime import date

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


def test_new_education():
    """
    GIVEN an education model,
    WHEN a new education object is created,
    THEN check school_name, major, status_id, user_id are correct.
    """
    data = ["한국대학교", "디자인학과", 1, 2]
    educ = Education(data[0], data[1], data[2], data[3])
    assert educ.school_name == data[0]
    assert educ.major == data[1]
    assert educ.status_id == data[2]
    assert educ.user_id == data[3]


def test_new_award():
    """
    GIVEN an award model,
    WHEN a new award object is created,
    THEN check name, description, user_id are correct.
    """
    data = ["개근상", "상받았다.", 1]
    award = Award(data[0], data[1], data[2])
    assert award.name == data[0]
    assert award.description == data[1]
    assert award.user_id == data[2]


def test_new_project():
    """
    GIVEN a project model,
    WHEN a new project object is created,
    THEN check name, description, start_date, end_date, user_id are correct
    """
    data = ["엘리스프로젝트", "포트폴리오 만들기 프로젝트.", date(2021, 1, 1), date(2021, 12, 24), 1]
    project = Project(data[0], data[1], data[2], data[3], data[4])
    assert project.name == data[0]
    assert project.description == data[1]
    assert project.start_date == data[2]
    assert project.end_date == data[3]
    assert project.user_id == data[4]


def test_new_cert():
    """
    GIVEN a Certification model,
    WHEN a new cert object is created,
    THEN check name, provider, acquired_date, user_id are correct.
    """
    data = ["요리자격증", "국가요리원", date(2021, 1, 1), 1]
    cert = Certification(data[0], data[1], data[2], data[3])
    assert cert.name == data[0]
    assert cert.provider == data[1]
    assert cert.acquired_date == data[2]
    assert cert.user_id == data[3]
