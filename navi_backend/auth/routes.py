import time
from datetime import datetime, timezone

from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from .models import UserModel
from flask_restx import Namespace, Resource, reqparse
from flask_jwt_extended import create_access_token, set_access_cookies, get_jwt, jwt_required, get_jwt_identity, set_refresh_cookies, get_csrf_token
from flask import Response
from datetime import timedelta

namespace = Namespace('auth', description='', path='/api/v1/auth')

parser = reqparse.RequestParser()
parser.add_argument('login', type=str, help='username')
parser.add_argument('password', type=str, help='password')


@namespace.route('/login/<login>/<password>', )
@namespace.doc(params={
    'login': 'Login',
    'password': 'Password'
})
class Auth(Resource):

    @namespace.doc('auth', responses={200: 'Authorization successful.', 401: 'Bad username or password.'})
    def post(self, login, password):
        user = UserModel.query.filter_by(username=login).first()
        if user is None or not user.check_password(password):
            return jsonify({'message': 'authorization failed'}, 401)
        access_token = create_access_token(identity=user.username)
        res = jsonify({'message': 'login successful'})
        set_access_cookies(res, access_token)
        set_refresh_cookies(res, access_token)
        # self.update_token_info(user)
        return res

    @staticmethod
    @jwt_required()
    def update_token_info(user: UserModel) -> None: # tu bedzie storowanie tokenów do bazy, timestampy z odswiezenia itp
        jwt = get_jwt()
        user.token = jwt
        user.created = jwt['s']
        user.updated = ''
        user.expires = jwt["exp"]
        user.save()


@namespace.route('/refresh', )
class RefreshToken(Resource):

    @jwt_required()
    @namespace.doc('refresh', responses={200: 'OK'})
    def get(self):
        jwt = get_jwt()
        try:
            exp_timestamp = jwt["exp"]
            now = datetime.now(timezone.utc)
            response = jsonify({'message': 'refresh successful'})
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return jsonify(access_token=jwt)




