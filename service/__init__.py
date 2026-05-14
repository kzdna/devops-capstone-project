from flask import Flask
from flask_talisman import Talisman
from service.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Exercise 4: Menambahkan Talisman untuk keamanan headers
talisman = Talisman(app)

db.init_app(app)

# Import routes di akhir untuk menghindari circular import
from service import routes  # noqa: F401, E402