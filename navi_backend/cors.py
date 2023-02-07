from flask_cors import CORS


class NaviCors(CORS):

    def __int__(self):
        super().__init__()

    @classmethod
    def health_check(cls):
        pass

