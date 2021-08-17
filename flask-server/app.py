from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from db_connect import db  # import SQLAlchemy object
from models import User

# Extensions to initialize with app
db_migration = Migrate()
bcrypt = Bcrypt()

# Create a Flask instance
app = Flask(__name__)

# Configs
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost/elice_portfolio_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "BLKJSSLDIJLJFLKSJDFLIJ"

# Initializations
db.init_app(app)
db_migration.init_app(app, db)
bcrypt.init_app(app)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/test")
def testMigration():
    user = User("aaa", "asdfasdf", "Yulie")
    db.session.add(user)
    db.session.commit()
