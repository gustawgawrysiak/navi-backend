from flask_restx.namespace import Namespace
from flask_restx import Resource
from .exceptions import RoomsNotFound
from .rooms_dto import FEATURE_COLLECTION_MODEL
from faculty.models.room_model import RoomModel
from typing import TypedDict
from json import loads, dumps
from flask.json import jsonify
from geojson import Feature, FeatureCollection
from flask_jwt_extended import jwt_required



api = Namespace('rooms', description='', path='/api/v1/rooms')



api.errorhandler(RoomsNotFound(description="query did not match any rooms"))


@api.route('/room/<int:faculty_id>/<room_id>', endpoint='/room')
@api.response(404, 'Room not found')
@api.doc(params={
    'faculty_id': 'Faculty identifier',
    'room_id': 'Room identifier'
})
class Room(Resource):

    @api.doc('get_room', responses={200: 'OK'})
    def get(self, faculty_id: int, room_id: str, ):
        query = RoomModel.query.filter_by(faculty_id=faculty_id,
                                          room_id=room_id).first()
        return jsonify(query.serialize)


@api.route('/<int:faculty_id>/<int:floor_id>', endpoint='')
@api.response(404, 'Rooms not found')
@api.doc(params={
    'faculty_id': 'Faculty identifier',
    'floor_id': 'Floor identifier'
            })
class Rooms(Resource):

    @api.doc('get_room', responses={200: 'OK', 401: 'Unauthorized'})
    @jwt_required()
    def get(self, faculty_id: int, floor_id: int):
        query = RoomModel.query.filter_by(faculty_id=faculty_id,
                                          floor_id=floor_id)
        res = []
        for room in query:
            res.append(room.serialize)
        return jsonify(FeatureCollection(features=res))
