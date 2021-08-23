from flask_login import login_required, current_user
from . import user_details_blueprint
from flask import json, jsonify, current_app, request
from project.models import User, Education, Award, Project, Certification
from project import db
from datetime import date, datetime

NOT_AUTHORIZED = {"result": 0, "message": "Not authorized."}

######################
# HELPERS
######################
def parse_date_helper(data):
    """
    Goes through list of attributes and values.
    If attribute name ends with "_date",
    Parse into date format.
    """
    parsed = []
    for prop in data:
        if prop[0].endswith("_date"):
            try:
                date = datetime.strptime(prop[1], "%Y-%m-%d").date()
                parsed.append(date)
            except ValueError:
                parsed.append(prop[1])
                continue
        else:
            parsed.append(prop[1])

    current_app.logger.debug(f"parsed list: {parsed}")
    return parsed


def post_details_helper(new_data, model, current_user_id):
    """
    For new data, model type, and user id received,
    Creates a new model instance with the new data and
    Commits the model to the database.
    """
    try:
        parsed = parse_date_helper(new_data)
        print("parsed: ", parsed)
        new_detail = model(*parsed, current_user_id)
        print(new_detail.status_id)
        db.session.add(new_detail)
        db.session.commit()
        current_app.logger.debug(f"Created Model: {new_detail.to_dict()}")

        data_return = {
            "result": 1,
            "message": f"{type(new_detail).__name__} created.",
            "id": new_detail.id,
        }
        return jsonify(data_return)
    except:
        db.session.rollback()
        return (
            jsonify({"result": 0, "message": f"Failed to create {model.__name__}."}),
            500,
        )


def edit_details_helper(edit_data, model, detail_id):
    """
    For edit data received for a particular model record,
    Edit the record with the edit data
    and commit the change to the database.
    """
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


def user_id_authorized(user_id, current_user_id):
    if user_id != current_user_id:
        return 0
    return 1


def detail_id_authorized_for_user(model, current_user_id, detail_id):
    detail_row = db.session.query(model).filter_by(id=detail_id).first()
    if detail_row and detail_row.user_id == current_user_id:
        return 1
    return 0


###################
# ROUTES
##################


@user_details_blueprint.route("/users/<int:user_id>")
def get_user_details(user_id):
    user = User.query.filter_by(id=user_id).first()

    educations = [edu.to_dict() for edu in user.educations]
    awards = [award.to_dict() for award in user.awards]
    projects = [proj.to_dict() for proj in user.projects]
    certifications = [cert.to_dict() for cert in user.certifications]

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


@user_details_blueprint.route("/users/<int:user_id>/educations", methods=["POST"])
@login_required
def post_education_detail(user_id):
    """
    GETS: [school_name, major, status]
    RETURNS: {result: 1, message: "Education created.", education_id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    new_data = request.json
    print("NEW DATA", new_data)
    return post_details_helper(new_data, Education, current_user.id)


@user_details_blueprint.route(
    "/users/<int:user_id>/educations/<int:id>", methods=["PATCH"]
)
@login_required
def edit_education_detail(user_id, id):
    """
    GETS: [(ANY) school_name, major, status, education_id]
    RETURNS: {result: 1, message: "Education updated", education_id: 1}
    """

    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Education, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    edit_data = request.json
    return edit_details_helper(edit_data, Education, id)


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
    GETS:   [(ANY) name, description, education_id]
    RETURNS: {result: 1, message: "Award updated.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Award, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    edit_data = request.json
    return edit_details_helper(edit_data, Award, id)


@user_details_blueprint.route("/users/<int:user_id>/projects", methods=["POST"])
@login_required
def post_project_detail(user_id):
    """
    GETS: [name, description, start_date, end_date]
    RETURNS: {result: 1, message: "Project created.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    new_data = request.json
    return post_details_helper(new_data, Project, 1)


@user_details_blueprint.route(
    "/users/<int:user_id>/projects/<int:id>", methods=["PATCH"]
)
@login_required
def edit_project_detail(user_id, id):
    """
    GETS:   [ (ANY) name, description, start_date, end_date ]
    RETURNS: {result: 1, message: "Project updated.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Project, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    edit_data = request.json
    return edit_details_helper(edit_data, Project, id)


@user_details_blueprint.route("/users/<int:user_id>/certifications", methods=["POST"])
@login_required
def post_certification_detail(user_id):
    """
    GETS: [name, provider]
    RETURNS: {result: 1, message: "Certification created.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    new_data = request.json
    return post_details_helper(new_data, Certification, current_user.id)


@user_details_blueprint.route(
    "/users/<int:user_id>/certifications/<int:id>", methods=["PATCH"]
)
@login_required
def edit_certification_detail(user_id, id):
    """
    GETS:   [ (ANY) name, provider, acquired_date ]
    RETURNS: {result: 1, message: "Certification updated.", id: 1}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Certification, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    edit_data = request.json
    return edit_details_helper(edit_data, Certification, id)
