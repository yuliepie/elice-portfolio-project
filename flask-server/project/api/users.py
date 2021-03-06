from . import users_blueprint
from flask import json, request, jsonify, current_app
from project.models import User
from project import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
import click


@users_blueprint.route("/")
def index():
    return jsonify({"result": "success"})


# Register new user & log in
@users_blueprint.route("/users", methods=["POST"])
def register():
    try:
        user_data = request.json

        new_user = User(
            user_data.get("email"), user_data.get("password"), user_data.get("name")
        )
        db.session.add(new_user)
        db.session.commit()

        # log the user in straight away and send user data.
        login_user(new_user)
        return jsonify(
            {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
            }
        )
    except IntegrityError:
        db.session.rollback()
        return "Existing user.", 401
    except:
        db.session.rollback()
        return "Failed registration.", 500


# Login user
@users_blueprint.route("/login", methods=["POST"])
def login():
    # Check already logged in
    if current_user.is_authenticated:
        current_app.logger.info(
            f"Duplicate login attempt by user: {current_user.email}"
        )
        return jsonify({"result": 0, "message": "already logged in."})

    login_data = request.json
    user = User.query.filter_by(email=login_data.get("email")).first()
    if user and user.is_password_correct(login_data.get("password")):
        # valid credentials - log in user
        login_user(user, remember=True)
        current_app.logger.info(f"Logged in user: {current_user.email}")
        return {
            "result": 1,
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
            },
            "message": "login success",
        }

    return jsonify({"result": 0, "message": "invalid credentials"}), 401


# Logout user
@users_blueprint.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"Logged out user: {current_user.email}")
    logout_user()
    return jsonify({"result": 1, "message": "logout success"})


# View all users
@users_blueprint.route("/users")
@login_required
def view_users():
    search_query = request.args.get("name", type=str)
    if search_query:
        print(search_query)
        users = db.session.query(
            User.id, User.name, User.description, User.imagePath
        ).filter(
            (User.name.like("%" + search_query + "%")) & (User.id != current_user.id)
        )
    else:
        users = (
            db.session.query(User.id, User.name, User.description, User.imagePath)
            .filter(User.id != current_user.id)
            .all()
        )

    result = [dict(user) for user in users]
    return jsonify(
        {
            "users": result,
        }
    )


@users_blueprint.route("/whoami")
def check_current_user():
    if current_user.is_authenticated:
        return jsonify(
            {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name,
            }
        )
    return "Not logged in.", 401


######################
#### cli commands ####
######################

# flask users create_default_users
@users_blueprint.cli.command("create_default_users")
def create_default_users():
    """Create three new users and add them to the database"""
    user1 = User("john@app.com", "12341234", "?????????")
    user1.description = "??????????????? ??????????????????!!!"
    user2 = User("sally@app.com", "12341234", "?????????")
    user2.description = "??????????????? ??????????????????!!!"
    user3 = User("peter@app.com", "12341234", "?????????")
    user3.description = "??????????????? ??????????????????!!!"
    db.session.add_all([user1, user2, user3])
    db.session.commit()


# flask users create_default_users
@users_blueprint.cli.command("create_many_users")
def create_many_users():
    user1 = User("john1@app.com", "12341234", "?????????")
    user1.description = "??????????????? ??????????????????!!!"
    user2 = User("sally1@app.com", "12341234", "?????????")
    user2.description = "??????????????? ??????????????????!!!"
    user3 = User("peter1@app.com", "12341234", "?????????")
    user3.description = "??????????????? ??????????????????!!!"
    user4 = User("john2@app.com", "12341234", "?????????")
    user4.description = "??????????????? ??????????????????!!!"
    user5 = User("sally2@app.com", "12341234", "?????????")
    user5.description = "??????????????? ??????????????????!!!"
    user6 = User("peter2@app.com", "12341234", "?????????")
    user6.description = "??????????????? ??????????????????!!!"
    user7 = User("john3@app.com", "12341234", "?????????")
    user7.description = "??????????????? ??????????????????!!!"
    user8 = User("sally3@app.com", "12341234", "?????????")
    user8.description = "??????????????? ??????????????????!!!"
    user9 = User("peter3@app.com", "12341234", "?????????")
    user9.description = "??????????????? ??????????????????!!!"
    db.session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9])
    db.session.commit()


@users_blueprint.cli.command("delete_users")
def delete_users():
    """Clear all user records from table."""
    db.session.query(User).delete()
    db.session.commit()


@users_blueprint.cli.command("create_user")
@click.argument("email")
@click.argument("pw")
@click.argument("name")
@click.argument("desc")
def create(email, pw, name, desc):
    """Create a new user and add it to the database"""
    user = User(email, pw, name)
    user.description = desc
    db.session.add(user)
    db.session.commit()
