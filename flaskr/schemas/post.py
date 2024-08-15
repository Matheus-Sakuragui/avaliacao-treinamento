from flaskr.schema import ma
from marshmallow import fields, Schema
from flaskr.schemas.comment import CommentSchema
from flaskr.schemas.like import LikeSchema

class PostSchema(ma.Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author_id = fields.Int()
    comments = fields.Nested(CommentSchema, many=True)
    likes = fields.Nested(LikeSchema, many=True)
    
    class Meta:
        fields = ("id", "title", "body", "author_id", "comments", "likes")
        ordered = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("post")
        }
    )


class PostRequestSchema(Schema):
    title = fields.Str(required=True, default='title', help='This field cannot be blank')
    body = fields.Str(required=True, default='body', help='This field cannot be blank')
    
class PostRequestPutSchema(Schema):
    id = fields.Int(required=True, default='id', help='Invalid id')
    title = fields.Str(required=True, default='title', help='This field cannot be blank')
    body = fields.Str(required=True, default='body', help='This field cannot be blank')
    
class PostRequestGetSchema(Schema):
    id = fields.Int(required=True, default='id', help='Invalid id')
    
class PostRequestByAuthorIdSchema(Schema):
    author_id = fields.Int(required=True, default='author_id', help='Invalid author_id')

post_schema = PostSchema()

    
