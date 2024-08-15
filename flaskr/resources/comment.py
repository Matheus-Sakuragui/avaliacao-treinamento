from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields

from flaskr.models.comment import CommentModel
from flaskr.schemas.token import MessageSchema
from flaskr.schemas.comment import (comment_schema, CommentRequestGetSchema, CommentRequestSchema, CommentRequestByPostIdSchema)
from flaskr.models.token import TokenBlocklistModel
from flask_jwt_extended import decode_token

@doc(description='Comment Register API', tags=['Comment'])
class CommentRegisterResource(MethodResource, Resource):
    @use_kwargs({
    'access_key':
    fields.Str(
        required=True,
        description='access_key'
    )
}, location='query')
    @marshal_with(comment_schema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(CommentRequestSchema, location='json')
    @doc(description='Register a new comment')
    def post(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        
        author_id = claims["sub"]
        comment = CommentModel(**kwargs, author_id=author_id)
        if comment.save():
            return make_response(comment_schema.dump(comment), 201)
        return make_response({"message": "Fail registering new comment"}, 400)
    
    @use_kwargs({
    'access_key':
    fields.Str(
        required=True,
        description='access_key'
    )
}, location='query')
    @marshal_with(MessageSchema, code=204)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='json')
    @doc(description='Delete comment by id')
    def delete(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        author_id = claims["sub"]
        comment = CommentModel.getCommentById(kwargs['id'])
        if comment:
            if comment.author_id != author_id:
                return make_response({"message": "Not authorized to delete this post"}, 401)
            comment.delete()
            return make_response({"message": "Comment deleted"}, 204)
        return make_response({"message": "Comment not found"}, 404)