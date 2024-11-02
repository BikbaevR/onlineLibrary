from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('tags/', UserTagListView.as_view(), name='usertag_list'),
    path('tags/<int:pk>/', UserTagDetailView.as_view(), name='usertag_detail'),
    path('tags/create/', UserTagCreateView.as_view(), name='usertag_create'),
    path('tags/<int:pk>/update/', UserTagUpdateView.as_view(), name='usertag_update'),
    path('tags/<int:pk>/delete/', UserTagDeleteView.as_view(), name='usertag_delete'),
]