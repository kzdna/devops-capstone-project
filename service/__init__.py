from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS  # <--- 1. Tambahkan import ini
from service.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inisialisasi Keamanan
talisman = Talisman(app)
CORS(app)  # <--- 2. Tambahkan baris ini biar CORS aktif!

db.init_app(app)

# Import routes di akhir untuk menghindari circular import
from service import routes  # noqa: F401, E402