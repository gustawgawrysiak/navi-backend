import os

import redis
from flask import Flask
from navi_backend.cors import NaviCors
from navi_backend.api import NaviAPI
import logging
from datetime import datetime
from navi_backend.auth.routes import namespace as auth_namespace
from navi_backend.db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from flask_ipfilter import IPFilter, Whitelist
from redis import Redis, StrictRedis
from navi_backend.whitelist import Whitelist

version = '0.97'


log = logging.getLogger(__name__)


now = datetime.now()


app = Flask(__name__)
app.config.from_object(Config)


cache = redis.Redis(host='localhost', port=6379, db=0)


# whitelist = Whitelist()
# whitelist.evaluate('127.0.0.1')
# whitelist.import_from_file()

# ip_filter = IPFilter(app, ruleset=whitelist)

cors = NaviCors(app)

api = NaviAPI(app,
              title='Navi backend',
              version=version,
              description=f'Navi backend API',
              doc='/api/docs',
              url_scheme=f'{Config.FLASK_RUN_HOST}:{Config.FLASK_RUN_PORT}/',
              license_url='essa?',
              terms_url='',
              contact_url='sssss'
              )
jwt = JWTManager(app)

from faculty.api.namespaces.rooms import api as rooms_namespace
from faculty.api.namespaces.faculty import api as floors_namespace

api.add_namespace(ns=rooms_namespace)
api.add_namespace(ns=floors_namespace)
api.add_namespace(ns=auth_namespace)


db.init_app(app)
migrate = Migrate(app, db)
if __name__ == '__main__':
    app.run()
