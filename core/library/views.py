from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import *
from .forms import *

from .tools import for_context



class IndexView(View):
    def get(self, request):
        for_context(self)
        return render(request, 'library/index.html')


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
    template_name = 'library/tags/usertag_form.html'
    success_url = reverse_lazy('usertag_list')


class UserTagDeleteView(DeleteView):
    model = UserTag
    template_name = 'library/tags/usertag_confirm_delete.html'
    success_url = reverse_lazy('usertag_list')

