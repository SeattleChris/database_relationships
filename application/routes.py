from flask import current_app as app
from flask import render_template, redirect, url_for, request, flash  # , abort
from .models import Student, Book, Year, Locker, Classroom, Subject, Grade, Club
# from . import forms
# from .models import db
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


@app.route('/<string:mod>/<int:id>')
def view(mod, id):
    """ Used to view the Model represented by 'mod', with database id of 'id'. """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    model = Model.query.get(id)
    if not model:
        flash("That record does not exist")
        model = {'id': 0}
    template = 'view.html'
    return render_template(template, mod=mod, data=model)


@app.route("/<string:mod>/add", methods=['GET', 'POST'])
def add(mod):
    """ Create a new Student or other Model """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    form = Model.form
    if request.method == 'POST':
        app.logger.info(f'--------- add {mod}------------')
        data = request.form.to_dict(flat=True)  # TODO: add form validate method for security.
        # TODO: ?Check for failing unique column fields, or failing composite unique requirements?
        model = Model(**data)
        return redirect(url_for('view', mod=mod, id=model['id']))
    # template = f"{mod}_form.html"
    template, related = 'form.html', {}
    if mod == 'campaign':
        template = f"{mod}_{template}"
        # TODO: Modify query to only get the id and name fields?
        users = model_db.User.query.all()
        brands = model_db.Brand.query.all()
        related['users'] = [(ea.id, ea.name) for ea in users]
        related['brands'] = [(ea.id, ea.name) for ea in brands]
    return render_template(template, action='Add', mod=mod, data={}, related=related)


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


# Catchall redirect route.
@app.route('/<string:page_name>/')
def render_static(page_name):
    """ Catch all for undefined routes. Return the requested static page. """
    # if page_name == 'favicon.ico':
    #     return abort(404)
    return render_template('%s.html' % page_name)
