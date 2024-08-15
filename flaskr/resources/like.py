from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields

from flaskr.models.like import LikeModel
from flaskr.schemas.token import MessageSchema
from flaskr.schemas.like import (like_schema, LikeRequestGetSchema, LikeRequestSchema)
from flaskr.models.token import TokenBlocklistModel
from flask_jwt_extended import decode_token

@doc(description='Like Register API', tags=['Like'])
class LikeRegisterResource(MethodResource, Resource):
    @use_kwargs({
    'access_key':
    fields.Str(
        required=True,
        description='access_key'
    )
}, location='query')
    @marshal_with(like_schema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(LikeRequestSchema, location='json')
    @doc(description='Register a new like')
    def post(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        author_id = claims["sub"]
        like = LikeModel(**kwargs, author_id=author_id)
        if like.save():
            return make_response(like_schema.dump(like), 201)
        return make_response({"message": "Fail registering new like"}, 400)
    
    @marshal_with(like_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='json')
    @doc(description='Get like by id')
    def get(self, **kwargs):
        like = LikeModel.getLikesByPostId(kwargs['id'])
        if like:
            return make_response(like_schema.dump(like), 200)
        return make_response({"message": "Like not found"}, 404)
    
    
    @use_kwargs({
    'access_key':
    fields.Str(
        required=True,
        description='access_key'
    )
}, location='query')
    @marshal_with(MessageSchema, code=204)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='json')
    @doc(description='Delete like by id')
    def delete(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        author_id = claims["sub"]
        like = LikeModel.getById(kwargs['id'])
        if like:
            if like.author_id != author_id:
                return make_response({"message": "You are not the author of this like"}, 401)
            like.delete()
            return make_response({"message": "Like deleted"}, 204)
        return make_response({"message": "Like not found"}, 404)