from app import db


class Faculty(db.Model):
    __tablename__ = 'wnozigp_final'
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer)
    name_pl = db.Column(db.String(128))
    name_en = db.Column(db.String(128))
    name_uk = db.Column(db.String(128))
