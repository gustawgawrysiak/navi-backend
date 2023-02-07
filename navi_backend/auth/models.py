from navi_backend.db import db
import hashlib


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.TEXT)
    token = db.Column(db.TEXT)
    created = db.Column(db.TEXT)
    updated = db.Column(db.TEXT)
    expires = db.Column(db.TEXT)
    scope = db.Column(db.TEXT)
    password = db.Column(db.TEXT)

    def check_password(self, password) -> bool:
        salt = b'Q\x7f\xa9/\xe7\x10\xc1\xb9\x8e\xd7j\x9c;m\xf7\xd01k\rF\x8d\x88\xd3\x08&\x93U\xac\xd4\xd0\xed\x13'
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ) != self.password
