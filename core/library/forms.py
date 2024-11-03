from django import forms
from .models import UserTag, Genre, Book


class UserTagForm(forms.ModelForm):
    class Meta:
        model = UserTag
        fields = ['tag_name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'price', 'description', 'image', 'rating', 'pages', 'genres', 'file']

