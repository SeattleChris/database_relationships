from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import BaseQuery, SQLAlchemy  # if we create custom query
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from datetime import datetime as dt
from dateutil import parser
from pprint import pprint  # only for debugging
# TODO: see "Setting up Constraints when using the Declarative ORM Extension" at https://docs.sqlalchemy.org/en/13/core/constraints.html#unique-constraint

db = SQLAlchemy()


def init_app(app):
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)  # Disabled since it unnecessary uses memory
    # app.config.setdefault('SQLALCHEMY_ECHO', True)  # Turns on A LOT of logging.
    # app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'  # Perhaps already set by default in MySQL
    db.init_app(app)


def _create_database():
    """ May currently only work if we do not need to drop the tables before creating them """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        # db.drop_all()
        # print("All tables dropped!")
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()