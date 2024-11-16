from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, TemplateView

from accounts.views import email_verified_required
from .models import *
from .forms import *

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    if UserHistory.objects.filter(user=user, book=book).exists():
        messages.warning(request, "Вы уже купили эту книгу!")
        return redirect('book_detail', pk=book_id)

    if user.money >= book.price:
        user.money -= book.price
        user.save()

        UserHistory.objects.create(user=user, book=book)
        messages.success(request, "Книга успешно куплена!")
    else:
        messages.error(request, "Недостаточно средств для покупки этой книги!")

    return redirect('book_detail', pk=book_id)


class AdminView(ListView):
    model = Book
    template_name = 'library/admin.html'
    context_object_name = 'books'

    @method_decorator(email_verified_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    #     context = self.get_context_data(**kwargs)
    #     return render(request, 'library/admin.html', context)



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
        user = self.request.user


        if user.is_authenticated:
            context['in_favorite'] = Favorite.objects.filter(user=user, book=self.object).exists()
            context['is_purchased'] = UserHistory.objects.filter(user=user, book=self.object).exists()
        else:
            context['in_favorite'] = False
            context['is_purchased'] = False

        context['comments'] = Comment.objects.filter(book=self.object)
        context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = self.object
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('book_detail', args=[self.object.pk]))
        return self.get(request, *args, **kwargs)


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


class BookSearchView(ListView):
    model = Book
    template_name = 'library/book/book_search.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all()

        search_query = self.request.GET.get('search', '')
        genre_filter = self.request.GET.getlist('genre', [])
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query)
            )

        if genre_filter:
            queryset = queryset.filter(genres__id__in=genre_filter).distinct()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_year:
            queryset = queryset.filter(year__gte=min_year)
        if max_year:
            queryset = queryset.filter(year__lte=max_year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context


class ReadBook(DetailView):
    model = Book
    template_name = 'library/book/book_read.html'
    context_object_name = 'book_read'


