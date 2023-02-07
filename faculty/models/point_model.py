from navi_backend.db import db
import json
from geojson import Feature, Point, Polygon
from faculty.api.namespaces.faculty_dto import ROOMS_MAP
from typing import List


class PointModel(db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer(), primary_key=True)
    latitude = db.Column(db.DECIMAL)
    longitude = db.Column(db.DECIMAL)
    category_id = db.Column(db.Integer)
    category = db.Column(db.TEXT)
    floor_id = db.Column(db.Integer)
    faculty_id = db.Column(db.Integer)
    # geom = db.Column(Geometry)

    # 0 - sala wykładowa,  1 - sala ćwiczeniowa,
    # 2 - pokój pracownika,  3 - dziekanat, 4 - winda,
    # 5 - administracyjne, 6 - łazienki, 7 - szatnia,
    # 8 - korytarze, 9 - biblioteka, 10 – inne
    @property
    def serialize(self) -> dict:
        return {
            'type': "Feature",
            'geometry': {
                    'type': "Point",
                    "coordinates": [
                        float(self.longitude),
                        float(self.latitude)]},
                    'properties': {
                                    'category': self.category,
                                    'floor_id': self.floor_id,
                                    'faculty_id': self.faculty_id
                                  },
                    'id': self.id
                }