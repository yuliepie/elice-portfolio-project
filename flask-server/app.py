from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from db_connect import db  # import SQLAlchemy object

db_migration = Migrate()

# Create a Flask instance
app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost/elice_portfolio_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "BLKJSSLDIJLJFLKSJDFLIJ"

db.init_app(app)
db_migration.init_app(app, db)

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return "Hello World!"
