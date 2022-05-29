from django.forms import ModelForm
from mentor.models import Invitation
from django import forms

class InviteForm(ModelForm):
    class Meta:
        model = Invitation
        fields = [ 'email', 'name', 'group']