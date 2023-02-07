import json
from flask_restx.namespace import Namespace
from flask_restx import Resource
from .exceptions import RoomsNotFound
from faculty.models.faculty_generic_model import FacultyGenericModel
from faculty.models.room_model import RoomModel
from faculty.models.point_model import PointModel
from flask.json import jsonify
from typing import Dict, Any, Optional
from geojson import Point, Polygon
from geojson import Feature
from flask import Response
from .faculty_dto import FeatureCollection, FacultyIDEnum, FloorCategoryType
from app import cache


api = Namespace('faculty', description='', path='/api/v1/faculty')


api.errorhandler(RoomsNotFound(description="query did not match any floor(s)"))


@api.route('/floor/<int:faculty_id>/<int:floor_id>', endpoint='/floor')
@api.doc(params={
    'faculty_id': 'Faculty identifier',
    'floor_id': 'Floor identifier',
})
class Floors(Resource):

    @api.doc('get_floor', responses={200: 'OK', 401: 'Unauthorized', 404: 'Room not found'})
    #@jwt_required()
    def get(self, faculty_id: int, floor_id: int):
        query = RoomModel.query.filter_by(faculty_id=faculty_id,
                                          floor_id=floor_id).all()
        res = FeatureCollection(features=[room.serialize for room in query])
        return jsonify(res)


@api.route('/<int:faculty_id>/', endpoint='/floors')
@api.doc(params={
    'faculty_id': 'Faculty identifier'
})
class FloorsList(Resource):

    @api.doc('get_floor', responses={200: 'OK', 401: 'Unauthorized', 404: 'Room not found'})
    #@jwt_required()
    def get(self, faculty_id: int) -> Response:
        cache_key = f'floors_list_{faculty_id}'
        #if cache.get(cache_key):
        #    return jsonify(
        #        json.loads(cache.get(cache_key).decode('utf-8'))
        #    )
        floors_query = RoomModel.query.filter_by(faculty_id=faculty_id).all() #filter_by(faculty_id=faculty_id).all()
        points_query = PointModel.query.filter_by(faculty_id=faculty_id).all()
        floors_map: Dict[int: Dict[str, FeatureCollection[Feature[Any[Point, Polygon]]]]] = {}
        for room in floors_query:
            floor_id = room.floor_id
            if floor_id not in floors_map:
                floors_map[floor_id] = {}
                floors_map[floor_id][FloorCategoryType.rooms] = FeatureCollection(features=[])
                floors_map[floor_id][FloorCategoryType.points] = FeatureCollection(features=[])
            else:
                floors_map[floor_id][FloorCategoryType.rooms].append_feature(room.serialize)

        for point in points_query:
            floors_map[point.floor_id]['points'].append_feature(point.serialize)

        cache.set(cache_key, json.dumps(floors_map))
        return jsonify(floors_map)


@api.route('/<name_id>/', endpoint='/floors/name')
@api.doc(params={
    'name_id': 'Name identifier'
})
class FloorsListByName(Resource):

    @api.doc('get_floor_by_name', responses={200: 'OK', 401: 'Unauthorized', 404: 'Room not found'})
    #@jwt_required()
    def get(self, name_id: str) -> Response:
        faculty_id = getattr(FacultyIDEnum, name_id)
        cache_key = f'floors_list_{faculty_id}'
        if cache.get(cache_key):
            return jsonify(
                json.loads(cache.get(cache_key).decode('utf-8'))
            )
        query = RoomModel.query.filter_by(faculty_id=faculty_id).all() #filter_by(faculty_id=faculty_id).all()
        floors_map: Dict[int: FeatureCollection[Feature]] = {}
        for room in query:
            floor_id = room.floor_id
            if floor_id not in floors_map:
                floors_map[floor_id] = FeatureCollection(features=[])
            else:
                floors_map[floor_id].append_feature(room.serialize)
        cache.set(cache_key, json.dumps(floors_map))
        return jsonify(floors_map)


@api.route('/generic/<int:university_id>/<name_id>/', endpoint='/faculty/generic')
@api.doc(params={
    'university_id': 'University identifier',
    'name_id': 'Name identifier'
})
class FacultyGeneric(Resource):

    @api.doc('get_faculty_generic', responses={200: 'OK', 401: 'Unauthorized', 404: 'Generic model not found'})
    def get(self, university_id: int, name_id: str):
        cache_key = f'faculty_generic_{university_id}_{name_id}'
        if cache.get(cache_key):
            return jsonify(
                json.loads(cache.get(cache_key).decode('utf-8'))
            )
        query = FacultyGenericModel.query.filter_by(
            university_id=university_id,
            name_id=name_id).first()

        faculty_feature = query.serialize

        cache.set(cache_key, json.dumps(faculty_feature))
        return jsonify(faculty_feature)


@api.route('/generic/<int:university_id>/', endpoint='/university/generic')
@api.doc(params={
    'university_id': 'University identifier'
})
class UniversityGenericModel(Resource):

    @api.doc('get_university_generic_model', responses={200: 'OK', 401: 'Unauthorized', 404: 'Generic model not found'})
    def get(self, university_id: int):
        cache_key = f'university_generic_{university_id}'
        if cache.get(cache_key):
            return jsonify(
                json.loads(cache.get(cache_key).decode('utf-8'))
            )
        query = FacultyGenericModel.query.filter_by(
            university_id=university_id).all()
        university: FeatureCollection[Feature] = FeatureCollection(features=[])
        for faculty in query:
            university.append_feature(feature=faculty.serialize)
        cache.set(cache_key, json.dumps(university))
        return jsonify(university)
