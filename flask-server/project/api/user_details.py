from . import user_details_blueprint
from flask import jsonify


@user_details_blueprint.route("/details")
def index():
    return jsonify({"result": "success"})
