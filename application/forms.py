# from . import models
from .models import Student, Book, Year, Locker, Classroom, Subject, Grade, Club
from wtforms_alchemy import ModelForm, ModelFormField, ModelFieldList, QuerySelectField
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


# def available_lockers():
#     found = Locker.query.filter(Locker.student.is_type(Student)).all()
#     print(found)
#     for locker in found:
#         print(isinstance(locker.student, Student))
#         print(locker.student)
#     return Locker.query.filter(Locker.student is not None)


def valid_years():
    return Year.query


class StudentForm(ModelForm):
    class Meta:
        model = Student

    # locker_id = QuerySelectField(query_factory=available_lockers, allow_blank=True)
    locker_id = SelectField('Assigned Locker', coerce=int)
    # books = SelectMultipleField('Textbooks Assigned')
    # books = ModelFieldList(FormField(BookForm))
    year = QuerySelectField(query_factory=valid_years, get_label='graduation_year')
    # year = ModelFormField(YearForm)
    # rooms = ModelFormField(ClassroomForm)
    # subjects = ModelFormField(SubjectForm)
