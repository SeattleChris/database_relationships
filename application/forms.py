# from . import models
from .models import Student, Book, Year, Locker, Classroom, Subject, Grade, Club
from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms.fields import SelectField

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


def valid_books():
    # filter out if book already assigned.
    return Book.query


def valid_rooms():
    return Classroom.query


def valid_subjects():
    return Subject.query


def all_students():
    return Student.query


def all_clubs():
    return Club.query


class SubjectForm(ModelForm):
    class Meta:
        model = Subject

    students = QuerySelectMultipleField(query_factory=all_students)  # get_label=<some Model field>


class StudentForm(ModelForm):
    class Meta:
        model = Student

    # locker_id = QuerySelectField(query_factory=available_lockers, allow_blank=True)
    locker_id = SelectField('Assigned Locker', coerce=int)
    year_id = SelectField('Class of', coerce=int)
    subjects = QuerySelectMultipleField(query_factory=valid_subjects)  # get_label=<some Model field>
    books = QuerySelectMultipleField(query_factory=valid_books)  # get_label=<some Model field>
    rooms = QuerySelectMultipleField(query_factory=valid_rooms)  # get_label=<some Model field>
    high_regards = QuerySelectMultipleField(query_factory=all_students)  # get_label=<some Model field>
    leading_clubs = QuerySelectMultipleField(query_factory=all_clubs)  # get_label=<some Model field>
    joined_clubs = QuerySelectMultipleField(query_factory=all_clubs)  # get_label=<some Model field>
    # books = ModelFieldList(FormField(BookForm))
    # rooms = ModelFormField(ClassroomForm)
