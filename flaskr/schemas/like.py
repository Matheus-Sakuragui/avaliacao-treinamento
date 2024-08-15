from marshmallow import Schema, fields

from flaskr.schema import ma

class LikeSchema(ma.Schema):
    id = fields.Int()
    post_id = fields.Int()
    author_id = fields.Int()
    
    class Meta:
        fields = ("id", "post_id", "author_id")
        ordered = True
        
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("like")
        }
    )
    
class LikeRequestSchema(ma.Schema):
    post_id = fields.Int(required=True, default='post_id', help='This field cannot be blank')

class LikeRequestGetSchema(ma.Schema):
    id = fields.Int(required=True, default='id', help='Invalid id')
    
like_schema = LikeSchema()