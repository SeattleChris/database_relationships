from . import models
from wtforms_alchemy import ModelForm

# https://wtforms-alchemy.readthedocs.io/en/latest/introduction.html


class StudentForm(ModelForm):
    class Meta:
        model = models.Student
