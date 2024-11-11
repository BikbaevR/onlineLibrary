from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView

from accounts.views import email_verified_required
from .models import *
from .forms import *

from .tools import for_context


class AdminView(ListView):
    model = Book
    template_name = 'library/admin.html'
    context_object_name = 'books'


class IndexView(ListView):
    model = Book
    template_name = 'library/index.html'
    context_object_name = 'books'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_favorite'] = Favorite.objects.filter(user=self.request.user, book=self.object).exists()
        return context


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


class BuyBookView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        if request.user.money >= book.price:
            request.user.money -= book.price
            request.user.save()

            UserHistory.objects.create(user=request.user, book=book)

            statistic, created = Statistic.objects.get_or_create(user=request.user)
            statistic.shopping += 1
            statistic.save()

            messages.success(request, f'Вы успешно купили книгу "{book.title}"!')
        else:
            messages.error(request, 'У вас недостаточно средств для покупки.')

        return redirect('book_detail', pk=book.id)


class AddToFavoritesView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        favourite = Favorite.objects.filter(user=request.user, book=book)
        if len(favourite) == 0:
            Favorite.objects.create(user=request.user, book=book)
            statistic, created = Statistic.objects.get_or_create(user=request.user, defaults={'shopping': 0, 'comments': 0, 'favorites': 0})
            statistic.favorites += 1
            statistic.save()

            # messages.success(request, f'Книга "{book.title}" добавлена в избранное!')

        return redirect('book_detail', pk=book.id)


class Favourites(ListView):
    model = Favorite
    template_name = 'library/utils/favorite_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(Favorite.objects.filter(user=self.request.user))
        favourites = Favorite.objects.filter(user=self.request.user)

        for favourite in favourites:
            context['favorites'] = Book.objects.filter(id=favourite.book.id)
        return context


class RemoveFromFavoritesView(View):
    def post(self, request, pk):
        print(pk)
        favourite = Favorite.objects.get(book__pk=pk, user__pk=request.user.id)
        if favourite is not None:
            print('asdasdasd')
            favourite.delete()
            print('asdasdasdas')
            return redirect('book_detail', pk=pk)
        return redirect('book_detail', pk=pk)
