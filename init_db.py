from service import app
from service.models import db

with app.app_context():
    db.create_all()
    print("Database Berhasil Dibuat!")
