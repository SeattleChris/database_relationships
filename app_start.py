import logging
from flask import Flask, render_template, abort, request, flash, redirect, url_for  # , current_app
import json
from os import environ


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.debug = debug
    app.testing = testing
    if config_overrides:
        app.config.update(config_overrides)
    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)
    # Setup the data model.
    with app.app_context():
        models = model_db
        models.init_app(app)

    # routes

    @app.route("/")
    def index():
        return "Index!"


    @app.route("/hello")
    def hello():
        return "Hello World!"


    @app.route("/members")
    def members():
        return "Members"


    @app.route("/members/<string:name>/")
    def getMember(name):
        return f"Members: {name}"