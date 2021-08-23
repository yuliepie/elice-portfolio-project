from flask import json, current_app
import pytest
from project import db
from project.models import Education, Award, Project, Certification


def test_fetch_user_details(test_client, add_new_user_and_details):
    """
    GIVEN a flask test app
    WHEN request is made to '/users/<:id>' (GET)
    THEN check response contains user detail data.
    """
    data, userid = add_new_user_and_details
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]

    educations = user_details["educations"]
    awards = user_details["awards"]
    projects = user_details["projects"]
    certifications = user_details["certifications"]

    assert response.status_code == 200
    assert response_data["result"] == 1

    # Check for content
    assert any(
        edu["school_name"] == data["edu1"][0]
        and edu["major"] == data["edu1"][1]
        and edu["education_status"] == "재학중"
        for edu in educations
    )
    assert any(
        edu["school_name"] == data["edu2"][0]
        and edu["major"] == data["edu2"][1]
        and edu["education_status"] == "학사졸업"
        for edu in educations
    )
    assert any(
        award["name"] == data["award1"][0] and award["description"] == data["award1"][1]
        for award in awards
    )
    assert any(
        award["name"] == data["award2"][0] and award["description"] == data["award2"][1]
        for award in awards
    )
    assert any(
        proj["name"] == data["proj1"][0]
        and proj["description"] == data["proj1"][1]
        and str(proj["start_date"]) == data["proj1"][2].strftime("%Y-%m-%d")
        and str(proj["end_date"]) == str(data["proj1"][3].strftime("%Y-%m-%d"))
        for proj in projects
    )
    assert any(
        proj["name"] == data["proj2"][0]
        and proj["description"] == data["proj2"][1]
        and proj["start_date"] == data["proj2"][2].strftime("%Y-%m-%d")
        and proj["end_date"] == data["proj2"][3].strftime("%Y-%m-%d")
        for proj in projects
    )
    assert any(
        cert["name"] == data["cert1"][0]
        and cert["provider"] == data["cert1"][1]
        and cert["acquired_date"] == data["cert1"][2].strftime("%Y-%m-%d")
        for cert in certifications
    )
    assert any(
        cert["name"] == data["cert2"][0]
        and cert["provider"] == data["cert2"][1]
        and cert["acquired_date"] == data["cert2"][2].strftime("%Y-%m-%d")
        for cert in certifications
    )


def test_post_valid_education_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app
    WHEN all fields for education are posted to 'users/<:id>/education' (POST) and the user is logged in
    THEN check response is success and returns id of the new education record.
    """
    userid = log_into_user_for_editing
    new_data = [["school_name", "새학교"], ["major", "새전공"], ["status_id", 1]]
    response = test_client.post(
        f"/api/users/{userid}/educations",
        data=json.dumps(new_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 1
    assert type(response_data["id"]) == int

    # Check added correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    educations = user_details["educations"]

    assert any(
        edu["school_name"] == "새학교"
        and edu["major"] == "새전공"
        and edu["education_status"] == "재학중"
        for edu in educations
    )


###################
# EDUCATION
###################


def test_post_education_details_when_not_authenticated(
    test_client, add_new_user_and_details
):
    """
    GIVEN a flask test app
    WHEN all fields for education are posted to 'users/<:id>/education' (POST) but the user is not logged in
    THEN check response is fail.
    """
    userid = add_new_user_and_details[1]
    new_data = [["school_name", "새학교"], ["major", "새전공"], ["status_id", 1]]

    response = test_client.post(
        f"/api/users/{userid}/educations",
        data=json.dumps(new_data),
        content_type="application/json",
    )

    assert response.status_code == 401


def test_post_education_details_when_not_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app,
    WHEN all fields for education are posted to 'users/<:id>/education' (POST) but the id does not match current user's id
    THEN check response is fail.
    """
    userid = log_into_user_for_editing
    new_data = [["school_name", "새학교"], ["major", "새전공"], ["status_id", 1]]
    current_app.logger.debug(f"logged_in_user: {userid}")

    response = test_client.post(
        f"/api/users/{userid+1}/educations",
        data=json.dumps(new_data),
        content_type="application/json",
    )
    current_app.logger.debug(f"RESPONSE: {response.get_data(as_text=True)}")
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert response_data["result"] == 0
    assert response_data["message"] == "Not authorized."


def test_edit_education_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app,
    WHEN all some field for education is sent to 'users/<:user_id>/education/<:id>' (PATCH) and the user is authorized,
    THEN check response is success.
    """
    userid = log_into_user_for_editing
    new_school_name = "전학간학교"

    # Get an education record for user
    edu_row = db.session.query(Education).filter_by(user_id=userid).first()
    current_app.logger.debug(f"edu_row: {edu_row.id}")

    edit_data = {"school_name": new_school_name}
    current_app.logger.debug(
        f"requesting to : /api/users/{userid}/educations/{edu_row.id}"
    )
    response = test_client.patch(
        f"/api/users/{userid}/educations/{edu_row.id}",
        data=json.dumps(edit_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["id"] == 1

    # Check edited correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    educations = user_details["educations"]

    assert any(edu["school_name"] == new_school_name for edu in educations)


def test_edit_education_details_when_not_authenticated(
    test_client, add_new_user_and_details
):
    """
    GIVEN a flask test app
    WHEN all fields for education are posted to 'users/<:user_id>/education/<:id>' (PATCH) but the user is not logged in
    THEN check response is fail.
    """
    userid = add_new_user_and_details[1]
    new_school_name = "전학간학교"
    edit_data = {"school_name": new_school_name}
    response = test_client.patch(
        f"/api/users/{userid}/educations/1",
        data=json.dumps(edit_data),
        content_type="application/json",
    )

    assert response.status_code == 401


def test_edit_education_details_when_not_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app,
    WHEN all some field for education is sent to 'users/<:user_id>/education/<:id>' (PATCH) but id does not match any education records of the user
    THEN check response is fail.
    """
    userid = log_into_user_for_editing
    new_school_name = "전학간학교"
    edit_data = {"school_name": new_school_name}
    response = test_client.patch(
        f"/api/users/{userid}/educations/999",
        data=json.dumps(edit_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401
    assert response_data["message"] == "Not authorized."


###################
# AWARDS
###################
def test_post_valid_award_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app
    WHEN all fields for an award are posted to 'users/<:id>/awards' (POST) and the user is logged in
    THEN check response is success and returns id of the new award record.
    """
    userid = log_into_user_for_editing
    new_data = [["name", "새수상"], ["description", "새수상내역"]]
    response = test_client.post(
        f"/api/users/{userid}/awards",
        data=json.dumps(new_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 1
    assert type(response_data["id"]) == int

    # Check added correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    data = user_details["awards"]

    assert any(row["name"] == "새수상" and row["description"] == "새수상내역" for row in data)


def test_edit_award_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app,
    WHEN all some field for award is sent to 'users/<:user_id>/awards/<:id>' (PATCH) and the user is authorized,
    THEN check response is success.
    """
    userid = log_into_user_for_editing
    new_data = "또하나의수상"

    # Get an award record for user
    row = db.session.query(Award).filter_by(user_id=userid).first()

    edit_data = {"name": new_data}
    current_app.logger.debug(f"requesting to : /api/users/{userid}/awards/{row.id}")
    response = test_client.patch(
        f"/api/users/{userid}/awards/{row.id}",
        data=json.dumps(edit_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["id"] == 1

    # Check edited correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    data = user_details["awards"]

    assert any(row["name"] == new_data for row in data)


###################
# PROJECTS
###################
def test_post_valid_project_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app
    WHEN all fields for an project are posted to 'users/<:id>/projects' (POST) and the user is logged in
    THEN check response is success and returns id of the new project record.
    """
    userid = log_into_user_for_editing
    new_data = [
        ["name", "새프로젝트"],
        ["description", "새프로젝트입니다"],
        ["start_date", "2020-01-01"],
        ["end_date", "2020-12-12"],
    ]

    response = test_client.post(
        f"/api/users/{userid}/projects",
        data=json.dumps(new_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 1
    assert type(response_data["id"]) == int

    # Check added correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    data = user_details["projects"]

    for proj in data:
        current_app.logger.debug(f"Project id: {proj['id']}")
        current_app.logger.debug(f"Project name: {proj['name']}")
        current_app.logger.debug(f"Project description: {proj['description']}")
        current_app.logger.debug(f"Project startdate: {proj['start_date']}")
        current_app.logger.debug(f"Project end: {proj['end_date']}")

    assert any(
        row["name"] == "새프로젝트"
        and row["description"] == "새프로젝트입니다"
        and row["start_date"] == "2020-01-01"
        and row["end_date"] == "2020-12-12"
        for row in data
    )


def test_edit_project_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app,
    WHEN all some field for project is sent to 'users/<:user_id>/projects/<:id>' (PATCH) and the user is authorized,
    THEN check response is success.
    """
    userid = log_into_user_for_editing
    new_data = "또하나의프로젝트"

    # Get an project record for user
    row = db.session.query(Project).filter_by(user_id=userid).first()

    edit_data = {"name": new_data}
    response = test_client.patch(
        f"/api/users/{userid}/projects/{row.id}",
        data=json.dumps(edit_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["id"] == 1

    # Check edited correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    data = user_details["projects"]

    assert any(row["name"] == new_data for row in data)


###################
# CERTIFICATIONS
###################
def test_post_valid_cert_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app
    WHEN all fields for a certification are posted to 'users/<:id>/certifications' (POST) and the user is logged in
    THEN check response is success and returns id of the new certification record.
    """
    userid = log_into_user_for_editing
    new_data = [
        ["name", "새자격증"],
        ["provider", "자격증발급자"],
        ["acquired_date", "2020-01-01"],
    ]
    response = test_client.post(
        f"/api/users/{userid}/certifications",
        data=json.dumps(new_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["result"] == 1
    assert type(response_data["id"]) == int

    # Check added correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    data = user_details["certifications"]

    assert any(
        row["name"] == "새자격증"
        and row["provider"] == "자격증발급자"
        and row["acquired_date"] == "2020-01-01"
        for row in data
    )


def test_edit_certification_details_when_authenticated_and_authorized(
    test_client, log_into_user_for_editing
):
    """
    GIVEN a flask test app,
    WHEN some field for a certification is sent to 'users/<:user_id>/certifications/<:id>' (PATCH) and the user is authorized,
    THEN check response is success.
    """
    userid = log_into_user_for_editing
    new_data = "수정할자격증"

    # Get an project record for user
    row = db.session.query(Project).filter_by(user_id=userid).first()

    edit_data = {"name": new_data}
    response = test_client.patch(
        f"/api/users/{userid}/certifications/{row.id}",
        data=json.dumps(edit_data),
        content_type="application/json",
    )
    response_data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert response_data["id"] == 1

    # Check edited correctly
    response = test_client.get(f"/api/users/{userid}")
    response_data = json.loads(response.get_data(as_text=True))
    user_details = response_data["user_details"]
    data = user_details["certifications"]

    assert any(row["name"] == new_data for row in data)
