from dataclasses import dataclass
from flask_restx import fields
from typing import List, Union, Optional
from flask_restx.namespace import Namespace


@dataclass
class Polygon:
    coordinates: List[List[float]]

@dataclass
class Point:
    x: float
    y: float #decimale itd


@dataclass
class Feature:
    type = "Feature"
    geometry: Union[Polygon, Point]
    #properties: Dict[str, Any[dict, list, str]]


@dataclass
class FeatureCollection:
    type = "FeatureCollection"
    features: Optional[List[Feature]] = None

    def append_feature(self, feature):
         self.features.append(Feature(geometry=feature.geometry))

POLYGON = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": fields.List(fields.List(fields.Float()))
    }

}

PROPERTIES = {
    "info": fields.String()
}

FEATURE_COLLECTION_MODEL = {
    "type": "FeatureCollection",
    "features": fields.List(fields.Nested(POLYGON)),
    "properties": {
        fields.List(fields.Nested(PROPERTIES))
    }

}


class NamespaceApi(Namespace):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.as_view = True
