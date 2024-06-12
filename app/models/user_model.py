from app.database import db
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import json

class User(db.Model,UserMixin):
    __tablename__ = "users"

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(128),nullable=False)
    roles=db.Column(db.String(50),nullable=False)

    def __init__(self,username,password,roles=["user"]):
        self.username=username
        self.password=generate_password_hash(password)
        self.roles=json.dumps(roles)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()
