from flask import make_response
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields

from flaskr.models.user import UserModel
from flaskr.schemas.token import MessageSchema
from flaskr.schemas.user import (UserRequestGetSchema, UserRequestPostSchema,
                                 UserResponseSchema, user_schema)

from flaskr.models.token import TokenBlocklistModel
from flask_jwt_extended import decode_token

@doc(description='User Register API', tags=['User'])
class UserRegisterResource(MethodResource, Resource):

    @marshal_with(UserResponseSchema, code=201)
    @marshal_with(MessageSchema, code=400)
    @use_kwargs(UserRequestPostSchema, location='json')
    @doc(description='Register a new user')
    def post(self, **kwargs):
        if UserModel.find_by_username(kwargs['username']):
            return make_response({"message": "Username already exists"}, 400)

        user = UserModel(**kwargs)
        if user.save():
            return make_response(user_schema.dump(user), 201)
        return make_response({"message": "Fail registering new user"}, 400)