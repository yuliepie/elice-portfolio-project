from flask import json


def test_fetch_user_details(test_client, add_user_details):
    """
    GIVEN a flask test app
    WHEN request is made to '/users/<:id>' (GET)
    THEN check response contains user detail data.
    """
    data = add_user_details
    response = test_client.get("/api/users/1")
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
