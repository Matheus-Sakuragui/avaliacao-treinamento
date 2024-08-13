from marshmallow import Schema, fields

from flaskr.schema import ma

class CommentSchema(ma.Schema):
    id = fields.Int()
    body = fields.Str()
    post_id = fields.Int()
    author_id = fields.Int()
    
    class Meta:
        fields = ("id", "body", "post_id", "author_id")
        ordered = True
        
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("comment")
        }
    )
    
class CommentRequestSchema(ma.Schema):
    body = fields.Str(required=True, default='body', help='This field cannot be blank')
    post_id = fields.Int(required=True, default='post_id', help='This field cannot be blank')
    author_id = fields.Int(required=True, default='author_id', help='This field cannot be blank')

class CommentRequestGetSchema(ma.Schema):
    id = fields.Int(required=True, default='id', help='Invalid id')
    
class CommentRequestByPostIdSchema(ma.Schema):
    post_id = fields.Int(required=True, default='post_id', help='Invalid post_id')  
    
comment_schema = CommentSchema()
  
    
