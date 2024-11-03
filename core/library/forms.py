from django import forms
from .models import UserTag, Genre


class UserTagForm(forms.ModelForm):
    class Meta:
        model = UserTag
        fields = ['tag_name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
