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


class PostModel(db_instance.Model, UserMixin):
    __versioned__ = {
        'exclude': ['created_at', 'updated_at']
    }
    __tablename__ = 'posts'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}
    
    id = db_instance.Column(db_instance.Integer, primary_key=True, index=True)
    title = db_instance.Column(db_instance.String(80))
    body = db_instance.Column(db_instance.String(120))
    author_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey('users.id'))
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now())
    updated_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id
        
    def __repr__(self):
        return "<PostModel(id={self.id!r}, title={self.title!r}), body={self.body!r}, author_id={self.author_id!r})>".format(self=self)
    
    @classmethod
    def getPosts(self):
        return db_instance.session.query(PostModel).all()
    
    @classmethod
    def getPostById(self, id):
        return db_instance.session.query(PostModel).filter_by(id=id).first()
    
    @classmethod
    def getPostByAuthorId(self, author_id):
        return db_instance.session.query(PostModel).filter_by(author_id=author_id).all()
    
    @db_persist
    def save(self):
        db_instance.session.add(self)
        
    @db_persist
    def delete(self):
        db_instance.session.delete(self)
        
sa.orm.configure_mappers()
    
    
    