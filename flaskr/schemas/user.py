from marshmallow import Schema, fields

from flaskr.schema import ma


class UserResponseSchema(ma.Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()

    class Meta:
        # Fields to expose
        fields = ("id", "username")
        ordered = True

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user")
        }
    )


class UserRequestPostSchema(Schema):
    email = fields.Str(required=True, default='user1@mail.com', help='This field cannot be blank')
    username = fields.Str(required=True, default='user1', help='This field cannot be blank')
    password_hash = fields.Str(required=True, default='pwd1', help='This field cannot be blank')


class UserRequestGetSchema(Schema):
    uid = fields.Int(required=True, default='id', help='Invalid id')


user_schema = UserResponseSchema()
user_post_schema = UserRequestPostSchema()
