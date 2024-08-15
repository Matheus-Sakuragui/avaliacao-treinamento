import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.sql import func
from flaskr.db import db_instance, db_persist
import flaskr.config_app as ca
from flaskr.models.user import UserModel
from flaskr.login_manager import login_manager

@login_manager.user_loader
def get_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()

class CommentModel(db_instance.Model, UserMixin):
    __versioned__ = {
        'exclude': ['created_at', 'updated_at']
    }
    __tablename__ = 'comments'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}
    
    id = db_instance.Column(db_instance.Integer, primary_key=True, index=True)
    body = db_instance.Column(db_instance.String(120))
    post_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey(f'{ca.DEFAULT_DB_SCHEMA}.posts.id', ondelete='CASCADE'), nullable=False)
    author_id = db_instance.Column(db_instance.Integer, db_instance.ForeignKey(f'{ca.DEFAULT_DB_SCHEMA}.users.id', ondelete='CASCADE'), nullable=False)
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now())
    updated_at = db_instance.Column(db_instance.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def __init__(self, body, post_id, author_id):
        self.body = body
        self.post_id = post_id
        self.author_id = author_id
    
    def __repr__(self):
        return "<CommentModel(id={self.id!r}, body={self.body!r}), post_id={self.post_id!r}, author_id={self.author_id!r}, likes={self.likes!r})>".format(self=self)
    
    @classmethod
    def getComments(self):
        return db_instance.session.query(CommentModel).all()
    
    @classmethod
    def getCommentById(self, id):
        return db_instance.session.query(CommentModel).filter_by(id=id).first()
    
    @classmethod
    def getCommentByPostId(self, post_id):
        return db_instance.session.query(CommentModel).filter_by(post_id=post_id).all()

    @classmethod
    def getCommentByAuthorId(self, author_id):
        return db_instance.session.query(CommentModel).filter_by(author_id=author_id).all()
    
    @db_persist
    def save(self):
        db_instance.session.add(self)
        
    @db_persist
    def delete(self):
        db_instance.session.delete(self)
sa.orm.configure_mappers()