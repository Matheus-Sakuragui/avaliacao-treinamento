import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy_history import make_versioned
from werkzeug.security import check_password_hash, generate_password_hash

import flaskr.config_app as ca
from flaskr.db import db_instance, db_persist
from flaskr.login_manager import login_manager

make_versioned(user_cls='UserModel')


@login_manager.user_loader
def get_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


class UserModel(db_instance.Model, UserMixin):
    __versioned__ = {
        'exclude': ['created_at', 'updated_at']
    }
    __tablename__ = 'users'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}

    id = db_instance.Column(db_instance.Integer, primary_key=True, index=True)
    username = db_instance.Column(db_instance.String(80))
    email = db_instance.Column(db_instance.String(120))
    password_hash = db_instance.Column(db_instance.String(200))
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now())
    updated_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __init__(self, username, password_hash, email):
        self.username = username
        self.set_password(password_hash)
        self.email = email

    def __repr__(self):
        return "<UserModel(id={self.id!r}, username={self.username!r}), pwd={self.password_hashword!r}, email={self.email!r})>".format(self=self)

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    @db_persist
    def save(self):
        db_instance.session.add(self)

    @db_persist
    def delete(self):
        db_instance.session.delete(self)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    @staticmethod
    def init_data():
        if db_instance.session.query(UserModel.id).count() == 0:
            for count_user in range(1, 6):
                user = UserModel(username="user" + str(count_user), password_hash="pwd" + str(count_user))
                user.save()


sa.orm.configure_mappers()
