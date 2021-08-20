from flask_login import login_required, current_user
from . import user_details_blueprint
from flask import json, jsonify, current_app, request
from project.models import User, Education, Award, Project, Certification
from project import db

NOT_AUTHORIZED = {"result": 0, "message": "Not authorized."}


@user_details_blueprint.route("/details")
def index():
    return jsonify({"result": "success"})


@user_details_blueprint.route("/users/<int:user_id>")
def get_user_details(user_id):
    user = User.query.filter_by(id=user_id).first()

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


def post_details_helper(new_data, model, current_user_id):
    try:
        print("here")

        new_detail = model(*new_data, current_user_id)
        db.session.add(new_detail)
        db.session.commit()
        current_app.logger.debug(f"model name: {model.__name__}")
        data_return = {
            "result": 1,
            "message": f"{type(new_detail).__name__} created.",
            "id": new_detail.id,
        }
        current_app.logger.debug(f"message: {data_return['message']}")
        return jsonify(data_return)
    except:
        db.session.rollback()
        return (
            jsonify({"result": 0, "message": f"Failed to create {model.__name__}."}),
            500,
        )


def user_id_authorized(user_id, current_user_id):
    if user_id != current_user_id:
        return 0
    return 1


@user_details_blueprint.route("/users/<int:user_id>/educations", methods=["POST"])
@login_required
def post_education_detail(user_id):
    """
    GETS: {school_name, major, status}
    RETURNS: {result: 1, message: "Education created.", education_id: 1}
    """
    current_app.logger.debug(f"user_id: {user_id}, current_user: {current_user.id}")
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    new_data = request.json
    return post_details_helper(new_data, Education, current_user.id)

    ############

    # if user_id != current_user.id:
    #     return jsonify({"result": 0, "message": "Not authorized."}), 401

    # try:
    #     new_data = request.json
    #     new_detail = Education(
    #         new_data.get("school_name"),
    #         new_data.get("major"),
    #         new_data.get("status_id"),
    #         current_user.id,
    #     )
    #     db.session.add(new_detail)
    #     db.session.commit()
    #     return jsonify(
    #         {
    #             "result": 1,
    #             "message": "Education created.",
    #             "education_id": new_detail.id,
    #         }
    #     )
    # except:
    #     db.session.rollback()
    #     return jsonify({"result": 0, "message": "Failed to create education."}), 500


def edit_details_helper(edit_data, model, detail_id):
    try:
        current_app.logger.debug(f"Trying edit...")
        current_app.logger.debug(f"")

        edit_row = db.session.query(model).filter_by(id=detail_id).first()
        current_app.logger.debug(f"row to edit: {edit_row}")

        for key, val in edit_data.items():
            setattr(edit_row, key, val)
        db.session.commit()
        return jsonify(
            {
                "result": 1,
                "message": f"{model.__name__} updated.",
                "id": edit_row.id,
            }
        )
    except:
        db.session.rollback()
        return (
            jsonify({"result": 0, "message": f"Failed to update {model.__name__}."}),
            500,
        )


def detail_id_authorized_for_user(model, current_user_id, detail_id):
    detail_row = db.session.query(model).filter_by(id=detail_id).first()
    if detail_row and detail_row.user_id == current_user_id:
        return 1
    return 0


@user_details_blueprint.route(
    "/users/<int:user_id>/educations/<int:id>", methods=["PATCH"]
)
@login_required
def edit_education_detail(user_id, id):
    """
    GETS:   {
                ANY of school_name, major, status
                education_id
            }
    RETURNS: {result: 1, message: "Education updated", education_id: 1}
    """

    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Education, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    edit_data = request.json
    return edit_details_helper(edit_data, Education, id)
    # ================================
    # Check authorization
    # if check_user_id_authorization(user_id, current_user):
    #     return jsonify(NOT_AUTHORIZED), 401
    # user_edu_list = [edu for edu in current_user.educations if edu.id == id]
    # if len(user_edu_list) == 0:
    #     return jsonify({"result": 0, "message": "Not authorized. 2."}), 401

    # edit_data = request.json
    # try:
    #     edit_row = db.session.query(Education).filter_by(id=id).first()
    #     for key, val in edit_data.items():
    #         setattr(edit_row, key, val)
    #     db.session.commit()
    #     return jsonify(
    #         {
    #             "result": 1,
    #             "message": "Education updated.",
    #             "education_id": edit_row.id,
    #         }
    #     )
    # except:
    #     db.session.rollback()
    #     return jsonify({"result": 0, "message": "Failed to update education."}), 500


@user_details_blueprint.route("/users/<int:user_id>/awards", methods=["POST"])
@login_required
def post_award_detail(user_id):
    """
    GETS: [name, description]
    RETURNS: {result: 1, message: "Award created.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    new_data = request.json
    return post_details_helper(new_data, Award, current_user.id)


@user_details_blueprint.route("/users/<int:user_id>/awards/<int:id>", methods=["PATCH"])
@login_required
def edit_award_detail(user_id, id):
    """
    GETS:   { (ANY) name, description, education_id }
    RETURNS: {result: 1, message: "Award updated.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Award, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    edit_data = request.json
    return edit_details_helper(edit_data, Award, id)
