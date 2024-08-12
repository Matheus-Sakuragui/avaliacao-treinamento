from sqlalchemy_history import make_versioned

from flaskr.plugin.flask_plugin import FlaskPlugin


def config_versioning():
    make_versioned(plugins=[FlaskPlugin()])
