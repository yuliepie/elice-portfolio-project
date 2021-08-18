from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os


#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions in the global scope.
# To be initialized with Flask App.
db = SQLAlchemy()
db_migration = Migrate()
bcrypt = Bcrypt()


######################################
#### Application Factory Function ####
######################################

"""
An application factory function needs to:
- Create the Flask application as an instance of the Flask class
- Set configuration variables
- Register the blueprints
- Configure the logger
"""


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    # TODO: Configure logging

    return app


def register_blueprints(app):
    # Import & register blueprints
    from project.api import users_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/api")


def initialize_extensions(app):
    db.init_app(app)
    db_migration.init_app(app, db)
    bcrypt.init_app(app)
