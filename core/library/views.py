from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView
from .models import *
from .forms import *

from .tools import for_context


class AdminView(TemplateView):
    template_name = 'library/admin.html'


class IndexView(View):
    def get(self, request):
        for_context(self)
        return render(request, 'library/index.html')

# Теги


class UserTagListView(ListView):
    model = UserTag
    template_name = 'library/tags/usertag_list.html'
    context_object_name = 'usertags'


class UserTagCreateView(CreateView):
    model = UserTag
    form_class = UserTagForm
    template_name = 'library/tags/usertag_form.html'
    success_url = reverse_lazy('usertag_list')


class UserTagDetailView(DetailView):
    model = UserTag
    template_name = 'library/tags/usertag_detail.html'
    context_object_name = 'usertag'


class UserTagUpdateView(UpdateView):
    model = UserTag
    form_class = UserTagForm
    template_name = 'library/tags/usertag_update.html'
    success_url = reverse_lazy('usertag_list')


class UserTagDeleteView(DeleteView):
    model = UserTag
    template_name = 'library/tags/usertag_confirm_delete.html'
    success_url = reverse_lazy('usertag_list')


# Жанры


class GenreListView(ListView):
    model = Genre
    template_name = 'library/genre/genre_list.html'
    context_object_name = 'genres'


class GenreCreateView(CreateView):
    model = Genre
    form_class = GenreForm
    template_name = 'library/genre/genre_form.html'
    success_url = reverse_lazy('genre_list')


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'library/genre/genre_detail.html'
    context_object_name = 'usertag'


class GenreUpdateView(UpdateView):
    model = Genre
    form_class = GenreForm
    template_name = 'library/genre/genre_update.html'
    success_url = reverse_lazy('genre_list')


class GenreDeleteView(DeleteView):
    model = Genre
    template_name = 'library/genre/genre_confirm_delete.html'
    success_url = reverse_lazy('genre_list')


#Книги


class BookListView(ListView):
    model = Book
    template_name = 'library/book/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book/book_detail.html'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book/book_form.html'
    success_url = reverse_lazy('book_list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book/book_update.html'
    success_url = reverse_lazy('book_list')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')