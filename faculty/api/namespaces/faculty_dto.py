from dataclasses import dataclass, make_dataclass
from enum import Enum
from geojson import FeatureCollection as FC
from geojson import Feature
from typing import List, Iterable


class FeatureCollection(FC):

    def __init__(self, features: List):
        super().__init__(features=features)

    def append_feature(self, feature: Feature) -> None:
        self.features.append(feature)


# 0 - sala wykładowa,  1 - sala ćwiczeniowa,
# 2 - pokój pracownika,  3 - dziekanat, 4 - winda,
# 5 - administracyjne, 6 - łazienki, 7 - szatnia,
# 8 - korytarze, 9 - biblioteka, 10 – inne


class StyleEnum(Enum):
    pass


@dataclass
class Colors:
    SW = '#'
    SC = '#'
    PP = "#"
    DZ = '#'


ROOMS_MAP = {
            0: "sw",
            1: "sc",
            2: "pp",
            3: "dz",
            4: "wi",
            5: "ad",
            6: "la",
            7: "sz",
            8: "ko",
            9: "bi",
            10: "in"
        }


class FacultyIDEnum:
    wnozigp = 1


@dataclass
class Min:
    x: float
    y: float


class BBox:

    def __init__(self, coordinates: List[str]):
        self.min = coordinates[0].split()
        self.max = coordinates[1].split()

    def get_list(self):
        return [float(e) for e in self.min] + [float(e) for e in self.max]


class FeatureCollectionType:
    _rooms = 'rooms'
    _points = 'poi'

    @property
    def rooms(self):
        return self._rooms

    @property
    def points(self):
        return self._points

    def __dir__(self) -> Iterable[str]:
        return [self._rooms, self._points]


@dataclass
class FloorCategoryType:
    rooms = 'rooms'
    points = 'points'
