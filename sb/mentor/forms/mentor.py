from django.forms import ModelForm
from mentor.models import Mentor
from django import forms

class MentorForm(ModelForm):
    class Meta:
        model = Mentor
        fields = [ 'fname', 'lname', 'surname', 'image']