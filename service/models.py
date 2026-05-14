from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    """Class representasi Account"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def serialize(self):
        """Mengubah model menjadi dictionary"""
        return {"id": self.id, "name": self.name}

    @classmethod
    def find(cls, account_id):
        """Mencari account berdasarkan ID"""
        return cls.query.get(account_id)

    def create(self):
        """Membuat account baru ke database"""
        db.session.add(self)
        db.session.commit()
