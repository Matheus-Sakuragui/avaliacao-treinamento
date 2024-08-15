from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskr.models.like import LikeModel
from flaskr.models.user import UserModel
from flaskr.models.post import PostModel
from flaskr.models.comment import CommentModel
from flaskr.models.token import TokenBlocklistModel
from flaskr.db import db_instance as db
import flask_login as login
from flaskr.views.admin_index_view import MyAdminIndexView

class CustomModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return False

    column_hide_backrefs = False
    def get_column_names(self, only_columns, excluded_columns):
        return [(c.key, c.name) for c in self.model.__table__.columns]

def config_flask_admin(app):
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Admin Example', index_view=MyAdminIndexView(), base_template='master.html', template_mode='bootstrap3')

    admin.add_view(CustomModelView(UserModel, db.session))
    admin.add_view(CustomModelView(LikeModel, db.session))
    admin.add_view(CustomModelView(PostModel, db.session))
    admin.add_view(CustomModelView(CommentModel, db.session))
    admin.add_view(CustomModelView(TokenBlocklistModel, db.session))

    return admin