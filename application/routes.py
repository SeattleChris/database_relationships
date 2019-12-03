from flask import current_app as app
from flask import render_template, redirect, url_for, request, abort, flash
from .models import db, Student, Book, Year, Locker, Classroom, Subject, Grade, Club
from sqlalchemy import inspect
from . import forms
# from .models import db
# import json
mod_list = [Student, Book, Year, Locker, Classroom, Subject, Grade, Club]
mod_lookup = {model.__name__.lower(): model for model in mod_list}
form_lookup = {model: getattr(forms, f"{model.__name__}Form") for model in mod_list}


def model_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


@app.route("/")
def home():
    return render_template('base.html')


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
    data = model_dict(model)
    return render_template(template, mod=mod, data=data)


@app.route("/<string:mod>/add", methods=['GET', 'POST'])
def add(mod):
    """ Create a new Student or other Model """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    Form = form_lookup[Model]
    form = Form(request.form)
    # l_id = request.form.get('locker_id')
    # if l_id:
    #     l_id = 3
    #     print(l_id)
    #     print(type(l_id))
    #     request.form.locker_id = l_id
    # new_data = request.form.get('locker_id')
    # print(new_data)
    # print(type(new_data))
    if request.method == 'POST' and form.validate():
        app.logger.info(f'--------- add {mod}------------')
        # data = request.form.to_dict(flat=True)  # TODO: add form validate method for security.
        # # TODO: ?Check for failing unique column fields, or failing composite unique requirements?
        # model = Model(**data)
        # data = {key: key.data for key in form}
        # model = Model(**data)
        model = Model(**request.form)
        db.session.add(model)
        db.session.commit()
        print(model.id)
        # Model.save()
        if form.validate():
            flash(f"Good Job!!!!!")
        return redirect(url_for('view', mod=mod, id=model.id))
    # template = f"{mod}_form.html"
    template, related = 'form.html', {}
    if mod == 'campaign':
        template = f"{mod}_{template}"
        # TODO: Modify query to only get the id and name fields?
        # users = model_db.User.query.all()
        # brands = model_db.Brand.query.all()
        # related['users'] = [(ea.id, ea.name) for ea in users]
        # related['brands'] = [(ea.id, ea.name) for ea in brands]
    # return render_template(template, action='Add', mod=mod, data={}, related=related)
    return render_template(template, mod=mod, form=form)


@app.route("/<string:mod>/<int:id>/edit", methods=['GET', 'POST'])
def edit(mod, id):
    """ Edit existing record for Student or other Model """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    Form = form_lookup[Model]
    form = Form(request.POST)
    print(form)
    return f"Edit {mod} Route for record with {id} primary key. "


@app.route("/<string:mod>/<int:id>/delete")
def delete(mod):
    """ Delete the record for Model indicated by 'mod' with a primary key of 'id'. """

    return f"Delete {mod} Route. For {id} record. "


@app.route("/<string:mod>/list", methods=['GET'])
def all(mod):
    """ Show all records of the Model represented by 'mod'. """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    models = Model.query.all()
    # model_db.all(Model=Model)
    return render_template('list.html', mod=mod, data=models)

    return f"Show All {mod} Route"


# Catchall redirect route.
@app.route('/<string:page_name>/')
def render_static(page_name):
    """ Catch all for undefined routes. Return the requested static page. """
    if page_name == 'favicon.ico':
        return abort(404)
    return render_template('%s.html' % page_name)
