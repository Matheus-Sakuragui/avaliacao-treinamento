from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields

from flaskr.models.post import PostModel
from flaskr.schemas.token import MessageSchema
from flaskr.schemas.post import (post_schema, PostRequestGetSchema, PostRequestSchema, PostRequestByAuthorIdSchema)

from flaskr.models.token import TokenBlocklistModel
from flask_jwt_extended import decode_token

@doc(description='Post Register API', tags=['Post'])
class PostRegisterResource(MethodResource, Resource):
    
    @use_kwargs({
        'access_key':
        fields.Str(
            required=True,
            description='access_key'
        )
    }, location='headers')
    @marshal_with(post_schema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(PostRequestSchema, location='json')
    @doc(description='Register a new post')
    def post(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        
        author_id = claims["sub"]
        
        post = PostModel(**kwargs, author_id=author_id)
        if post.save():
            return make_response(post_schema.dump(post), 201)
        return make_response({"message": "Fail registering new post"}, 400)
    
    @use_kwargs({
        'access_key':
        fields.Str(
            required=True,
            description='access_key'
        )
    }, location='headers')
    @marshal_with(post_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestGetSchema, location='json')
    @doc(description='Get post by id')
    def get(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        
        post = PostModel.find_by_id(kwargs['id'])
        if post:
            return make_response(post_schema.dump(post), 200)
        return make_response({"message": "Post not found"}, 404)
    @use_kwargs({
        'access_key':
        fields.Str(
            required=True,
            description='access_key'
        )
    }, location='headers')
    @marshal_with(post_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestSchema, location='json')
    @doc(description='Update post by id')
    def put(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        author_id = claims["sub"]
        post = PostModel.find_by_id(kwargs['id'])
        if post:
            if post.author_id != author_id:
                return make_response({"message": "Not authorized to update this post"}, 401)
            post.save(kwargs)
            return make_response(post_schema.dump(post), 200)
        return make_response({"message": "Post not found"}, 404)
    
    @use_kwargs({
        'access_key':
        fields.Str(
            required=True,
            description='access_key'
        )
    }, location='headers')
    @marshal_with(MessageSchema, code=204)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestGetSchema, location='json')
    @doc(description='Delete post by id')
    def delete(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        author_id = claims["sub"]
        post = PostModel.find_by_id(kwargs['id'])
        if post:
            if post.author_id != author_id:
                return make_response({"message": "Not authorized to delete this post"}, 401)
            post.delete()
            return make_response({"message": "Post deleted"}, 204)
        return make_response({"message": "Post not found"}, 404)

@doc(description='Post List API', tags=['Post'])
class PostListResource(MethodResource, Resource):
    @marshal_with(post_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @doc(description='List all posts')

    def get(self):
        posts = PostModel.getPosts()
        if posts:
            return make_response(post_schema.dump(posts, many=True), 200)
        return make_response({"message": "No post found"}, 404)

@doc(description='Post by Author API', tags=['Post'])
class PostByAuthorResource(MethodResource, Resource):
    @use_kwargs({
    'access_key':
    fields.Str(
        required=True,
        description='access_key'
    )
}, location='headers')
    @marshal_with(post_schema, code=200)
    @marshal_with(MessageSchema, code=404)
    @use_kwargs(PostRequestByAuthorIdSchema, location='json')
    @doc(description='List all posts by author id')
    def get(self, **kwargs):
        access_token = TokenBlocklistModel.get_token(kwargs['access_key'])
        if not access_token:
            return make_response({"message": "Invalid access token"}, 401)
        claims = decode_token(access_token)
        if not claims:
            return make_response({"message": "User not authenticated"}, 401)
        del kwargs['access_key']
        posts = PostModel.getPostByAuthorId(kwargs['author_id'])
        if posts:
            return make_response(post_schema.dump(posts, many=True), 200)
        return make_response({"message": "No post found"}, 404)
    
    

