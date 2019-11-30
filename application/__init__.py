import logging
from flask import Flask  # , g
# from flask_session import Session  # if we are using this, also install flask_session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):  # debug=False, testing=False, config_overrides=None
    app = Flask(__name__)
    # app.config.from_object(config)
    app.config.from_object(config)
    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)
    # Setup the database and other plugins
    db.init_app(app)
    # login_manager.init_app(app)
    with app.app_context():
        from . import routes  # noqa: F401
        db.create_all()
        # app.register_blueprint(auth.auth_bp)
        return app
