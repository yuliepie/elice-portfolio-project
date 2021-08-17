from flask import Flask

# Create a Flask instance
app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost/elice_portfolio_db"


@app.route("/")
def index():
    return "Hello World!"
