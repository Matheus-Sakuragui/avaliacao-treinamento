from marshmallow import Schema, fields

from flaskr.schema import ma

class PostSchema(ma.Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author_id = fields.Int()
    
    class Meta:
        # Fields to expose
        fields = ("id", "title", "body", "author_id")
        ordered = True

    # Smart hyperlinking
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("post")
        }
    )

class PostRequestSchema(ma.Schema):
    title = fields.Str(required=True, default='title', help='This field cannot be blank')
    body = fields.Str(required=True, default='body', help='This field cannot be blank')
    author_id = fields.Int(required=True, default='author_id', help='This field cannot be blank')
    
class PostRequestGetSchema(ma.Schema):
    id = fields.Int(required=True, default='id', help='Invalid id')

post_schema = PostSchema()

    
