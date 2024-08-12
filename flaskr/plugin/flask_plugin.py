"""
FlaskPlugin offers way of integrating Flask framework with
sqlalchemy-history. Flask-Plugin adds two columns for Transaction model,
namely `user_id` and `remote_addr`.

These columns are automatically populated when transaction object is created.
The `remote_addr` column is populated with the value of the remote address that
made current request. The `user_id` column is populated with the id of the
current_user object.

::

    from sqlalchemy_history.plugins import FlaskPlugin
    from sqlalchemy_history import make_versioned


    make_versioned(plugins=[FlaskPlugin()])
"""
from __future__ import absolute_import

from sqlalchemy_history.plugins.base import Plugin
from sqlalchemy_utils import ImproperlyConfigured

flask = None
try:
    import flask
    from flask import has_app_context, has_request_context, request
except ImportError:
    pass


def fetch_current_user_id():
    if has_request_context():
        from flask_login import current_user

        try:
            return current_user.id
        except AttributeError:
            return None
    return None


def fetch_remote_addr():
    if has_app_context() and has_request_context():
        return request.remote_addr
    return None


class FlaskPlugin(Plugin):
    def __init__(
        self,
        current_user_id_factory=None,
        remote_addr_factory=None
    ):
        self.current_user_id_factory = (
            fetch_current_user_id if current_user_id_factory is None
            else current_user_id_factory
        )
        self.remote_addr_factory = (
            fetch_remote_addr if remote_addr_factory is None
            else remote_addr_factory
        )

        if not flask:
            raise ImproperlyConfigured(
                'Flask is required with FlaskPlugin. Please install Flask by'
                ' running pip install Flask'
            )

    def transaction_args(self, uow, session):
        return {
            'user_id': self.current_user_id_factory(),
            'remote_addr': self.remote_addr_factory()
        }
