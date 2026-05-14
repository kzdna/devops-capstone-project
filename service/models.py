from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def serialize(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def find(cls, account_id):
        return cls.query.get(account_id)

    def create(self):
        db.session.add(self)
        db.session.commit()
