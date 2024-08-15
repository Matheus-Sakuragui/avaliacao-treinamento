import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy_history import make_versioned
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models.user import UserModel

import flaskr.config_app as ca
from flaskr.db import db_instance, db_persist
from flaskr.login_manager import login_manager

make_versioned(user_cls='UserModel')


@login_manager.user_loader
def get_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


class LikeModel(db_instance.Model, UserMixin):
    __versioned__ = {
        'exclude': ['created_at', 'updated_at']
    }
    __tablename__ = 'likes'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}
    
    id = db_instance.Column(db_instance.Integer, primary_key=True, index=True)
    post_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey(f'{ca.DEFAULT_DB_SCHEMA}.posts.id', ondelete='CASCADE'), nullable=False)
    author_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey(f'{ca.DEFAULT_DB_SCHEMA}.users.id', ondelete='CASCADE'), nullable=False)
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now())
    
    def __init__(self, post_id, author_id):
        self.post_id = post_id
        self.author_id = author_id
    
    def __repr__(self):
        return "<LikeModel(id={self.id!r}, post_id={self.post_id!r}), author_id={self.author_id!r})>".format(self=self)

    @classmethod
    def getLikesByPostId(self, post_id):
        return db_instance.session.query(LikeModel).filter_by(post_id=post_id).all()
    
    @classmethod
    def getById(self, id):
        return db_instance.session.query(LikeModel).filter_by(id=id).first()
    
    @db_persist
    def save(self):
        db_instance.session.add(self)
        
    @db_persist
    def delete(self):
        db_instance.session.delete(self)
sa.orm.configure_mappers()