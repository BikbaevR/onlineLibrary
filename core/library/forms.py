from django import forms
from .models import UserTag, Genre, Book, Comment


class UserTagForm(forms.ModelForm):
    tag_name = forms.CharField(
        label='Название тега',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserTag
        fields = ['tag_name']


class GenreForm(forms.ModelForm):
    name = forms.CharField(
        label='Название жанра',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Genre
        fields = ['name']


class BookForm(forms.ModelForm):
    title = forms.CharField(
        label='Название книги',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        label='Автор',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    year = forms.IntegerField(
        label='Год издания',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    price = forms.DecimalField(
        label='Цена',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    image = forms.ImageField(
        label='Изображение обложки',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    rating = forms.DecimalField(
        label='Рейтинг',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    pages = forms.IntegerField(
        label='Количество страниц',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    genres = forms.ModelMultipleChoiceField(
        label='Жанры',
        queryset=Genre.objects.all(),
    )
    file = forms.FileField(
        label='Файл книги',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'price', 'description', 'image', 'rating', 'pages', 'genres', 'file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш комментарий...',
                'rows': 3,
            }),
        }
        labels = {
            'comment': '',
        }