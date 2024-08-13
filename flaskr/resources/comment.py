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
}, location='headers')
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
}, location='headers')
    @marshal_with(comment_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='json')
    @doc(description='Get comment by id')
    def get(self, **kwargs):
        
        comment = CommentModel.find_by_id(kwargs['id'])
        if comment:
            return make_response(comment_schema.dump(comment), 200)
        return make_response({"message": "Comment not found"}, 404)
    
    @marshal_with(comment_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestSchema, location='json')
    @doc(description='Update comment by id')
    @jwt_required()
    def put(self, **kwargs):
        comment = CommentModel.find_by_id(kwargs['id'])
        if comment:
            comment.update(kwargs)
            return make_response(comment_schema.dump(comment), 200)
        return make_response({"message": "Comment not found"}, 404)
    
    @marshal_with(MessageSchema, code=204)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(CommentRequestGetSchema, location='json')
    @doc(description='Delete comment by id')
    @jwt_required()
    def delete(self, **kwargs):
        comment = CommentModel.find_by_id(kwargs['id'])
        if comment:
            comment.delete()
            return make_response({"message": "Comment deleted"}, 204)
        return make_response({"message": "Comment not found"}, 404)
    
@doc(description='Comment List API', tags=['Comment'])
class CommentListResource(MethodResource, Resource):
        @marshal_with(comment_schema, code=200)
        @marshal_with(MessageSchema, code=404)
        @doc(description='Get all comments')
        @jwt_required()
        def get(self):
            comments = CommentModel.getComments()
            if comments:
                return make_response(comment_schema.dump(comments, many=True), 200)
            return make_response({"message": "Comments not found"}, 404)
        
@doc(description='Comment List by Post API', tags=['Comment'])
class CommentListByPostResource(MethodResource, Resource):
        @marshal_with(comment_schema, code=200)
        @marshal_with(MessageSchema, code=404)
        @use_kwargs(CommentRequestByPostIdSchema, location='json')
        @doc(description='Get all comments by post id')
        @jwt_required()
        def get(self, **kwargs):
            comments = CommentModel.getCommentByPostId(kwargs['post_id'])
            if comments:
                return make_response(comment_schema.dump(comments, many=True), 200)
            return make_response({"message": "Comments not found"}, 404)
        
