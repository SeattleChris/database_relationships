# from . import models
from .models import Student, Book, Year, Locker, Classroom, Subject, Grade, Club
from wtforms_alchemy import ModelForm, QuerySelectMultipleField
from wtforms.fields import SelectField

# https://wtforms-alchemy.readthedocs.io/en/latest/introduction.html


class BookForm(ModelForm):
    class Meta:
        model = Book


class LockerForm(ModelForm):
    class Meta:
        model = Locker


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom


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


class YearForm(ModelForm):
    class Meta:
        model = Year

    # students = QuerySelectMultipleField(query_factory=all_students)  # get_label=<some Model field>


class GradeForm(ModelForm):
    class Meta:
        model = Grade

    subject_id = SelectField('Subject', coerce=int)
    student_id = SelectField('Student', coerce=int)


class SubjectForm(ModelForm):
    class Meta:
        model = Subject

    students = QuerySelectMultipleField(query_factory=all_students)  # get_label=<some Model field>


class ClubForm(ModelForm):
    class Meta:
        model = Club

    leaders = QuerySelectMultipleField(query_factory=all_students)  # get_label=<some Model field>
    members = QuerySelectMultipleField(query_factory=all_students)  # get_label=<some Model field>


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
