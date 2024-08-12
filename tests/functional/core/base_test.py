import os

from flask_testing import TestCase


class BaseTestCase(TestCase):

    def create_app(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        os.environ['DEFAULT_DATABASE_URL'] = 'sqlite:///' + os.path.join(basedir, 'testing.sqlite')
        os.environ['DEFAULT_DB_SCHEMA'] = ''

        from flaskr.app import app
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        return app

    def setUp(self):
        from sqlalchemy import inspect

        from flaskr.db import db_instance
        from flaskr.init_db import init_load_data

        engine = db_instance.get_engine()
        inspector = inspect(engine)

        for tbl in reversed(db_instance.metadata.sorted_tables):
            print('##### Dropped Table - ' + tbl.name)
            if inspector.has_table(tbl.name):
                tbl.drop(bind=engine)
        db_instance.create_all()
        init_load_data()
