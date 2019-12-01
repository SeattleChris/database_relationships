from . import models
from wtforms_alchemy import ModelForm

# https://wtforms-alchemy.readthedocs.io/en/latest/introduction.html


class StudentForm(ModelForm):
    class Meta:
        model = models.Student


class BookForm(ModelForm):
    class Meta:
        model = models.Book


class YearForm(ModelForm):
    class Meta:
        model = models.Year


class LockerForm(ModelForm):
    class Meta:
        model = models.Locker


class ClassroomForm(ModelForm):
    class Meta:
        model = models.Classroom


class SubjectForm(ModelForm):
    class Meta:
        model = models.Subject


class GradeForm(ModelForm):
    class Meta:
        model = models.Grade


class ClubForm(ModelForm):
    class Meta:
        model = models.Club
