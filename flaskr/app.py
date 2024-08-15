from dotenv import load_dotenv
from flask import Flask

import flaskr.config_app as config
from flaskr.db import config_sql_alchemy, db_instance
from flaskr.init_db import init_load_data
from flaskr.login_manager import init_login_manager
from flaskr.migrate import load_migrate
from flaskr.routes import config_app_routes
from flaskr.schema import config_marshmallow
from flaskr.security import config_app_cors, config_jwt_token
from flaskr.swagger_docs import config_swagger
from flaskr.versioning_db import config_versioning
from flaskr.admin import config_flask_admin

load_dotenv()

app = Flask(__name__)

app.config['BUNDLE_ERRORS'] = True
app.config['DEBUG'] = config.FLASK_DEBUG
app.config['SECRET_KEY'] = config.SECRET_KEY

# Config SQLAlchemy
config_sql_alchemy(app)
config_versioning()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_load_data()
    print('Initialized the database.')


# Config Marshmallow
config_marshmallow(app)

# Init Login Manager
init_login_manager(app)

# Config Flask JWT Extended
jwt = config_jwt_token(app)

# Config App CORS
config_app_cors(app)

# Config Swagger Documentation
docs = config_swagger(app)

# Config Flask Restful
api = config_app_routes(app, docs)

config_flask_admin(app)


# Load Flask Migrate
migrate = load_migrate(db_instance, app)


if __name__ == '__main__':
    app.run()
