# from . import models
from .models import Student, Book, Year, Locker, Classroom, Subject, Grade, Club
from wtforms_alchemy import ModelForm, ModelFormField, ModelFieldList
from wtforms.fields import FormField, SelectField, SelectMultipleField

# https://wtforms-alchemy.readthedocs.io/en/latest/introduction.html


class BookForm(ModelForm):
    class Meta:
        model = Book


class YearForm(ModelForm):
    class Meta:
        model = Year


class LockerForm(ModelForm):
    class Meta:
        model = Locker


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom


class SubjectForm(ModelForm):
    class Meta:
        model = Subject


class GradeForm(ModelForm):
    class Meta:
        model = Grade


class ClubForm(ModelForm):
    class Meta:
        model = Club


class StudentForm(ModelForm):
    class Meta:
        model = Student

    lockers = Locker.query.all()  # .filter(not Locker.student)
    locker_list = [(ea.id, ea.number) for ea in lockers if not ea.student]
    locker_id = SelectField('Assigned Locker', choices=locker_list, coerce=int)
    # locker = ModelFormField(LockerForm)
    related = Book.query.all()
    book_list = [(ea.id, ea.barcode) for ea in related if not ea.student_id]
    books = SelectMultipleField('Textbooks Assigned', choices=book_list)
    # books = ModelFieldList(FormField(BookForm))
    # year = ModelFormField(YearForm)
    # rooms = ModelFormField(ClassroomForm)
    # subjects = ModelFormField(SubjectForm)
