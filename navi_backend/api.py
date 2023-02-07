from flask_restx import Api


class NaviAPI(Api):

    def __init__(self, app_obj, **kwargs):
        super().__init__(app=app_obj, **kwargs)
