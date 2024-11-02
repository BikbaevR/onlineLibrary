from django import forms
from .models import UserTag


class UserTagForm(forms.ModelForm):
    class Meta:
        model = UserTag
        fields = ['tag_name']
