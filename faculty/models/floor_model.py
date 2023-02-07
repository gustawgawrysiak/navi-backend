from app.db import db


class Floor(db.Model):
    __tablename__ = 'floors'
    id = db.Column(db.Integer())
