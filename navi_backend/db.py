from flask_sqlalchemy import SQLAlchemy


class NaviDB(SQLAlchemy):

    def __init__(self):
        super().__init__()

    @classmethod
    def health_check(cls):
        pass


db = NaviDB()
