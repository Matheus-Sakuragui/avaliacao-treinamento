from flaskr.db import db_instance as db
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash
from flaskr.models.user import UserModel

class LoginForm(form.Form):
    username = fields.StringField(validators=[validators.InputRequired()], label='Nome do usuário')
    password_hash = fields.PasswordField(validators=[validators.InputRequired()], label='Senha')

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Usuário inválido')
        
        if not check_password_hash(user.password, self.password_hash.data):
            raise validators.ValidationError('Senha inválida')

    def get_user(self):
        user: UserModel = db.session.query(UserModel).filter_by(username=self.username.data).first()
        if user and check_password_hash(user.password_hash, self.password_hash.data):
            return user
        return None


class RegistrationForm(form.Form):
    username = fields.StringField(validators=[validators.InputRequired()], label='Nome do usuário')
    email = fields.EmailField(validators=[validators.InputRequired()], label='E-mail')
    password_hash = fields.PasswordField(validators=[validators.InputRequired()], label='Senha')

    def validate_login(self, field):
        if db.session.query(UserModel).filter_by(username=self.username.data).count() > 0:
            raise validators.ValidationError('Usuário duplicado')