from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields

from flaskr.models.like import LikeModel
from flaskr.schemas.token import MessageSchema
from flaskr.schemas.like import (like_schema, LikeRequestGetSchema, LikeRequestSchema)

@doc(description='Like Register API', tags=['Like'])
class LikeRegisterResource(MethodResource, Resource):
    @marshal_with(like_schema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(LikeRequestSchema, location='json')
    @doc(description='Register a new like')
    @jwt_required()
    def post(self, **kwargs):
        like = LikeModel(**kwargs)
        if like.save():
            return make_response(like_schema.dump(like), 201)
        return make_response({"message": "Fail registering new like"}, 400)
    
    @marshal_with(like_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='json')
    @doc(description='Get like by id')
    @jwt_required()
    def get(self, **kwargs):
        like = LikeModel.getLikesByPostId(kwargs['id'])
        if like:
            return make_response(like_schema.dump(like), 200)
        return make_response({"message": "Like not found"}, 404)
    
    @marshal_with(like_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestSchema, location='json')
    @doc(description='Update like by id')
    @jwt_required()
    def put(self, **kwargs):
        like = LikeModel.find_by_id(kwargs['id'])
        if like:
            like.update(kwargs)
            return make_response(like_schema.dump(like), 200)
        return make_response({"message": "Like not found"}, 404)
    
    @marshal_with(MessageSchema, code=204)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(LikeRequestGetSchema, location='json')
    @doc(description='Delete like by id')
    @jwt_required()
    def delete(self, **kwargs):
        like = LikeModel.find_by_id(kwargs['id'])
        if like:
            like.delete()
            return make_response({"message": "Like deleted"}, 204)
        return make_response({"message": "Like not found"}, 404)