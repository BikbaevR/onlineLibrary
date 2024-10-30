from django.shortcuts import render
from django.views import View


from .tools import for_context



class IndexView(View):
    def get(self, request):
        for_context(self)
        return render(request, 'library/index.html')



