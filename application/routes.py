from flask import current_app as app
from .models import db, Student, Book, Year, Locker, Classroom, Subject, Grade, Club


@app.route("/")
def index():
    return "Index!"


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/members")
def members():
    return "Members"


@app.route("/<string:mod>/add", methods=['GET', 'POST'])
def add(mod):
    """ Create a new Student or other Model """

    return f"Add {mod} Route"


@app.route("/members/<string:name>/")
def getMember(name):
    return f"Members: {name}"
