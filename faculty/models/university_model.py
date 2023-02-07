from app import db


class UniversityModel(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer(), primary_key=True)
    name_pl = db.Column(db.String(128))
    name_en = db.Column(db.String(128))
    name_uk = db.Column(db.String(128))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name_pl': self.name_pl,
            'name_en': self.name_en,
            'name_uk': self.name_uk
        }
