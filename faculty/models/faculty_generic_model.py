from navi_backend.db import db
import json
from geojson import Feature
from ..api.namespaces.faculty_dto import BBox


class FacultyGenericModel(db.Model):
    __tablename__ = 'faculty_generic_model'
    id = db.Column(db.Integer, primary_key=True)
    # geom = db.Column(db.TEXT)
    full_id = db.Column(db.TEXT)
    osm_id = db.Column(db.Integer)
    name_id = db.Column(db.TEXT)
    longitude = db.Column(db.FLOAT)
    latitude = db.Column(db.FLOAT)
    university_id = db.Column(db.Integer)
    geometry = db.Column(db.TEXT)
    bounding_box = db.Column(db.TEXT)

    @property
    def serialize(self) -> Feature:
        return Feature(type="Feature",
                       id=self.id,
                       geometry=json.loads(str(self.geometry)),
                       properties={
                            'full_id': self.full_id,
                            'osm_id': self.osm_id,
                            'name_id': self.name_id,
                            'lon': self.longitude,
                            'lat': self.latitude,
                            'university_id': self.university_id,
                           },
                       bounding_box=BBox(self.bounding_box.split(',')).get_list()
                       )
