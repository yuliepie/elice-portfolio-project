from . import user_details_blueprint
from flask import jsonify, current_app
from project.models import User
from project import db


@user_details_blueprint.route("/details")
def index():
    return jsonify({"result": "success"})


@user_details_blueprint.route("/users/<int:id>")
def get_user_details(id):
    user = User.query.filter_by(id=id).first()

    educations = [
        {
            "id": edu.id,
            "school_name": edu.school_name,
            "major": edu.major,
            "education_status": edu.edustatus.status_name,
        }
        for edu in user.educations
    ]
    awards = [
        {"name": award.name, "description": award.description} for award in user.awards
    ]
    projects = [
        {
            "id": proj.id,
            "name": proj.name,
            "description": proj.description,
            "start_date": proj.start_date.strftime("%Y-%m-%d"),
            "end_date": proj.end_date.strftime("%Y-%m-%d"),
        }
        for proj in user.projects
    ]
    certifications = [
        {
            "id": cert.id,
            "name": cert.name,
            "provider": cert.provider,
            "acquired_date": cert.acquired_date.strftime("%Y-%m-%d"),
        }
        for cert in user.certifications
    ]

    result = {
        "result": 1,
        "user_details": {
            "educations": educations,
            "awards": awards,
            "projects": projects,
            "certifications": certifications,
        },
    }
    return jsonify(result)
