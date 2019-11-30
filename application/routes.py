from flask import current_app as app
from flask import render_template  # , abort, request, flash, redirect, url_for
from .models import db, Student, Book, Year, Locker, Classroom, Subject, Grade, Club
# import json
mod_list = [Student, Book, Year, Locker, Classroom, Subject, Grade, Club]
mod_lookup = {model.__name__.lower(): model for model in mod_list}


@app.route("/")
def home():
    return render_template('base.html')


@app.route("/hello")
def hello():
    data = "You went to hello function!"
    return render_template('base.html', data=data)


@app.route("/members")
def members():
    return "Members"


@app.route('/<string:mod>/<int:id>')
def view(mod, id):
    """ Used to view the Model represented by 'mod', with database id of 'id'. """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    model = Model.query.get(id)
    template = 'view.html'
    return render_template(template, mod=mod, data=model)


@app.route("/<string:mod>/add", methods=['GET', 'POST'])
def add(mod):
    """ Create a new Student or other Model """

    return f"Add {mod} Route"


@app.route("/<string:mod>/<int:id>/edit", methods=['GET', 'POST'])
def edit(mod, id):
    """ Edit existing record for Student or other Model """

    return f"Edit {mod} Route for record with {id} primary key. "


@app.route("/<string:mod>/<int:id>/delete")
def delete(mod):
    """ Delete the record for Model indicated by 'mod' with a primary key of 'id'. """

    return f"Delete {mod} Route. For {id} record. "


@app.route("/<string:mod>/list", methods=['GET'])
def all(mod):
    """ Show all records of the Model represented by 'mod'. """

    return f"Show All {mod} Route"


@app.route("/members/<string:name>/")
def getMember(name):
    return f"Members: {name}"


# Catchall redirect route.
@app.route('/<string:page_name>/')
def render_static(page_name):
    """ Catch all for undefined routes. Return the requested static page. """
    # if page_name == 'favicon.ico':
    #     return abort(404)
    return render_template('%s.html' % page_name)
