import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy_history import make_versioned

import flaskr.config_app as ca
from flaskr.db import db_instance, db_persist
import hashlib
from flaskr.db import redis_instance

make_versioned(user_cls='UserModel')


class TokenBlocklistModel(db_instance.Model):
    __versioned__ = {}
    __tablename__ = 'token_block_list'
    __table_args__ = {"schema": ca.DEFAULT_DB_SCHEMA}

    id = db_instance.Column(db_instance.Integer, primary_key=True)
    jti = db_instance.Column(db_instance.String(36), nullable=False, index=True)
    created_at = db_instance.Column(db_instance.DateTime(timezone=True), nullable=False, default=func.now())
    TOKEN_EXPIRATION_TIME = 3600

    @classmethod
    def get_token(cls, jti):
        return db_instance.session.query(TokenBlocklistModel.id).filter_by(jti=jti).scalar()
    
    @classmethod
    def save_token(cls, token,):
        key = hashlib.md5(token.encode()).hexdigest()
        redis_instance.set(key , token, ex=cls.TOKEN_EXPIRATION_TIME)
        return key
    
    @classmethod
    def refresh_token_expiration(cls, key):
        token = redis_instance.get(key)
        if token:
            redis_instance.set(key, token, ex=cls.TOKEN_EXPIRATION_TIME)
    
    @classmethod
    def get_token(cls, key):
        access_token = redis_instance.get(key)
        if access_token:
            cls.refresh_token_expiration(key)
            return access_token
        else:
            return None
        
    @classmethod
    def delete_token(cls, key):
        redis_instance.delete(key)

    @db_persist
    def save(self):
        db_instance.session.add(self)


sa.orm.configure_mappers()
