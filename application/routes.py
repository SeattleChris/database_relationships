from flask import current_app as app
from flask import render_template, redirect, url_for, request, abort, flash
from .models import db, Student, Book, Year, Locker, Classroom, Subject, Grade, Club
from sqlalchemy import inspect
from . import forms

mod_list = [Student, Book, Year, Locker, Classroom, Subject, Grade, Club]
mod_lookup = {model.__name__.lower(): model for model in mod_list}
form_lookup = {model: getattr(forms, f"{model.__name__}Form") for model in mod_list}


def model_dict(obj, related_obj=True):
    attrs = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    if related_obj:
        relationships = inspect(obj).mapper.relationships.keys()
        print(relationships)
        print('---------------------')
        for related in relationships:
            print(related)
            vals = getattr(obj, related)
            if isinstance(vals, list):
                for val in vals:
                    print(val)
            attrs[related] = getattr(obj, related)
            print(attrs[related])
            print('---------------------')
    return attrs


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
    print(data)
    return render_template(template, mod=mod, data=data)


@app.route("/<string:mod>/add", methods=['GET', 'POST'])
def add(mod):
    """ Create a new Student or other Model """
    Model = mod_lookup.get(mod, None)
    if not Model:
        return f"No such route: {mod}", 404
    Form = form_lookup[Model]
    form = Form(request.form)
    if Model == Student:
        lockers = Locker.query.all()
        locker_list = [(ea.id, ea.number) for ea in lockers if not ea.student]
        form.locker_id.choices = locker_list
        years = Year.query.all()
        years_list = [(ea.id, ea.graduation_year) for ea in years]
        form.year_id.choices = years_list
    elif Model == Grade:
        subjects = Subject.query.all()
        subject_list = [(ea.id, ea) for ea in subjects]
        form.subject_id.choices = subject_list
        # Should setup some JS to repopulate students based on subject selection.
        students = Student.query.all()
        student_list = [(ea.id, f"{ea.name} in: {', '.join([subj.name for subj in ea.subjects])}") for ea in students]
        form.student_id.choices = student_list
    if request.method == 'POST' and form.validate():
        app.logger.info(f'-------- add {mod}-----------')
        related_models = {k: v.mapper.class_ for k, v in inspect(Model).relationships.items()}
        # If assign the Model.id when possible for a field, then relationships are all multi-item possabilities.
        multi = {k: v for k, v in request.form.to_dict(flat=False).items() if k in related_models}
        data = request.form.to_dict(flat=True)
        data.update(multi)
        print(data)
        for key, val in data.items():
            if key in related_models:
                Related = related_models[key]
                if isinstance(val, list):
                    found = [Related.query.get(int(ea)) for ea in val]
                else:
                    found = Related.query.get(int(val))
                print(found)
                data[key] = found
        model = Model(**data)
        db.session.add(model)
        db.session.commit()
        if form.validate():
            flash(f"Good Job!! You made {mod} record {model.id}: {model}")
        return redirect(url_for('view', mod=mod, id=model.id))
    # template = f"{mod}_form.html"
    template = 'form.html'
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
