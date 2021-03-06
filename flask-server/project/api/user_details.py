from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import user_details_blueprint
from flask import json, jsonify, current_app, request
from project.models import User, Education, Award, Project, Certification
from project import db
from datetime import date, datetime
import os

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


def validate_image_file(filename):
    if "." not in filename:
        return (False,)
    extension = filename.rsplit(".", 1)[1].lower()
    if extension not in {"png", "jpg", "jpeg"}:
        return (False,)
    else:
        return (True, extension)


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
        edit_row = db.session.query(model).filter_by(id=detail_id).first()

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


def delete_details_helper(delete_id, model):
    """
    For delete id received for a particular model,
    Delete the record and commit the change to the database.
    """
    try:
        delete_row = db.session.query(model).filter_by(id=delete_id).first()
        db.session.delete(delete_row)
        db.session.commit()
        return jsonify({"id": delete_id})
    except:
        db.session.rollback()
        return f"failed to delete data for {model.__name__}.", 500


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
            "description": user.description,
            "name": user.name,
            "image": user.imagePath,
        },
    }
    return jsonify(result)


@user_details_blueprint.route("/users/<int:user_id>", methods=["PATCH"])
@login_required
def edit_user_information(user_id):
    """
    GETS: { name, description }
    RETURNS: {name, description}
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    new_data = request.json
    print(new_data)
    new_name = new_data.get("name")
    new_description = new_data.get("description")

    try:
        user = User.query.filter_by(id=user_id).first()
        if new_name is not None and user.name != new_name:
            user.name = new_name
        if new_description is not None and user.description != new_description:
            user.description = new_description

        db.session.commit()
        return jsonify({"name": user.name, "description": user.description})
    except:
        db.session.rollback()
        return (
            jsonify({"result": "fail"}),
            500,
        )


@user_details_blueprint.route("/users/<int:user_id>/image", methods=["POST"])
@login_required
def upload_profile_image(user_id):
    """
    GETS: image file
    RETURNS: image path
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401

    if "profile_image" not in request.files:
        return "No file uploaded.", 404

    profile_image = request.files["profile_image"]
    if not profile_image or profile_image.filename == "":
        return "No file uploaded.", 404

    # If image exists and is valid
    isValidImage = validate_image_file(profile_image.filename)
    if isValidImage[0] == True:
        filename = current_user.email + "." + isValidImage[1]
        filepath = os.path.join(current_app.config["IMAGE_FOLDER"], filename)
        profile_image.save(filepath)

        try:
            relative_path = "./project"
            path_to_save = os.path.relpath(filepath, relative_path)
            user = User.query.filter_by(id=user_id).first()
            user.imagePath = path_to_save

            db.session.commit()
            current_app.logger.info(f"Saved image file at path: {filepath}")
            return jsonify({"filepath": filepath})
        except:
            db.session.rollback()
            return "Failed to save image.", 500
    else:
        return "Not a valid image.", 415


###################
# Education
###################


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


@user_details_blueprint.route(
    "/users/<int:user_id>/educations/<int:id>", methods=["DELETE"]
)
@login_required
def delete_education_detail(user_id, id):
    """
    GETS: { id }
    RETURNS: { id: deleted id }
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Education, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    return delete_details_helper(id, Education)


###################
# Award
###################


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


@user_details_blueprint.route(
    "/users/<int:user_id>/awards/<int:id>", methods=["DELETE"]
)
@login_required
def delete_award_detail(user_id, id):
    """
    GETS: { id }
    RETURNS: { id: deleted id }
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Award, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    return delete_details_helper(id, Award)


###################
# Project
###################


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
    return post_details_helper(new_data, Project, current_user.id)


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


@user_details_blueprint.route(
    "/users/<int:user_id>/projects/<int:id>", methods=["DELETE"]
)
@login_required
def delete_project_detail(user_id, id):
    """
    GETS: { id }
    RETURNS: { id: deleted id }
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Project, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    return delete_details_helper(id, Project)


###################
# Certification
###################


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


@user_details_blueprint.route(
    "/users/<int:user_id>/certifications/<int:id>", methods=["DELETE"]
)
@login_required
def delete_certification_detail(user_id, id):
    """
    GETS: { id }
    RETURNS: { id: deleted id }
    """
    if not user_id_authorized(user_id, current_user.id):
        return jsonify(NOT_AUTHORIZED), 401
    if not detail_id_authorized_for_user(Certification, current_user.id, id):
        return jsonify(NOT_AUTHORIZED), 401

    return delete_details_helper(id, Certification)


####################
# CLI COMMANDS
####################

# flask user_details create_educations
@user_details_blueprint.cli.command("create_educations")
def create_educations():
    db.session.query(Education).delete()
    db.session.commit()
    edu1 = Education("???????????????", "?????????", 1, 7)
    edu2 = Education("???????????????", "????????????", 2, 7)
    edu3 = Education("???????????????", "?????????", 4, 8)
    db.session.add_all([edu1, edu2, edu3])
    db.session.commit()


@user_details_blueprint.cli.command("create_awards")
def create_awards():
    db.session.query(Award).delete()
    db.session.commit()
    aw1 = Award("??????????????????", "??????????????? ???????????? ????????? ????????? 2007?????? ??????.", 7)
    aw2 = Award("????????????", "?????? ?????? ????????? ????????? ???????????? ???????????? ?????? ???. 2015?????? ??????.", 7)
    aw3 = Award("????????????", "???????????? ????????? ???????????? ?????? ?????? ????????? ????????? ?????? ?????????. 2020?????? ??????", 8)
    db.session.add_all([aw1, aw2, aw3])
    db.session.commit()


@user_details_blueprint.cli.command("create_projects")
def create_projects():
    db.session.query(Project).delete()
    db.session.commit()
    proj1 = Project(
        "??????????????????",
        "????????? ???????????? ???????????? ?????? ??????????????? ??????????????? ?????? ??????",
        date(2019, 3, 20),
        date(2019, 11, 11),
        7,
    )
    proj2 = Project(
        "????????? ????????????",
        "????????? ????????? ????????? ???????????? ????????? ??????. ???????????? ???????????? ??????.",
        date(2020, 6, 1),
        date(2020, 8, 27),
        7,
    )
    proj3 = Project(
        "???????????? ????????????",
        "????????? ?????? ????????????rpg??? ??????????????? ??????????????? ??????.",
        date(2018, 2, 12),
        date(2019, 9, 17),
        8,
    )
    db.session.add_all([proj1, proj2, proj3])
    db.session.commit()


@user_details_blueprint.cli.command("create_certifications")
def create_certs():
    db.session.query(Certification).delete()
    db.session.commit()
    cert1 = Certification("??????????????????", "?????????????????????", date(2019, 7, 25), 7)
    cert2 = Certification("???????????????", "??????????????????", date(2020, 12, 5), 7)
    cert3 = Certification("???????????????", "????????????????????????", date(2011, 2, 15), 8)
    db.session.add_all([cert1, cert2, cert3])
    db.session.commit()
