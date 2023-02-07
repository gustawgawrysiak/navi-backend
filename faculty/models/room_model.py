from navi_backend.db import db
import json
from geojson import Feature
from faculty.api.namespaces.faculty_dto import ROOMS_MAP
from typing import List


class RoomModel(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer(), primary_key=True)
    room_id = db.Column(db.String(10))
    floor_id = db.Column(db.Integer)
    geometry = db.Column(db.TEXT)
    faculty_id = db.Column(db.Integer)
    category = db.Column(db.Integer)
    workers = db.Column(db.ARRAY(db.String))
    moria = db.Column(db.Integer)
    interactive = db.Column(db.Boolean)
    name_id = db.Column(db.TEXT)
    room_tag = db.Column(db.TEXT)
    # geom = db.Column(Geometry)

    # 0 - sala wykładowa,  1 - sala ćwiczeniowa,
    # 2 - pokój pracownika,  3 - dziekanat, 4 - winda,
    # 5 - administracyjne, 6 - łazienki, 7 - szatnia,
    # 8 - korytarze, 9 - biblioteka, 10 – inne
    @property
    def serialize(self) -> Feature:
        return Feature(type="Feature",
                       geometry=json.loads(str(self.geometry)),
                       properties={
                            'faculty_id': self.faculty_id,
                            'floor_id': self.floor_id,
                            'room_id': self.room_id,
                            'workers': self.workers,
                            'category': self.category,
                            'plan': self.moria,
                            'style': self.style_enum(self.category),
                            'interactive': self.interactive,
                            'name_id': self.name_id,
                            'room_tag': self.room_tag if not None else ''
                           },
                       id=self.id if not None else ''
                       )

    @staticmethod
    def style_enum(style_id: int):
        return ROOMS_MAP.get(style_id, None)
