#from flask_restx.namespace import Namespace
#from flask_restx import Resource
#from faculty.models.university_model import UniversityModel
#from flask import jsonify
#
#
#namespace = Namespace('universities', description='', path='/api/v1/universities')
#
#
#@namespace.route('/', endpoint='/universities')
#class UniversitiesList(Resource):
#
#    @namespace.doc('get_universities', responses={200: 'OK', 401: 'Unauthorized'})
#    def get(self):
#        query = UniversityModel.query.all()
#        res = []
#        for uni in query:
#            res.append(uni.serialize)
#        return jsonify(res)
#
#
#@namespace.route('/university/<int:university_id>', endpoint='/universities')
#@namespace.doc(params={
#    'university_id': 'University identifier',
#})
#class UniversitiesList(Resource):
#
#    @namespace.doc('get_universities', responses={200: 'OK', 401: 'Unauthorized'})
#    def get(self, uni_id):
#        query = UniversityModel.query.filter_by(id=uni_id)
#        res = []
#        for uni in query:
#            res.append(uni.serialize)
#        return jsonify(res)
#
