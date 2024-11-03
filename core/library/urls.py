from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin-panel/', AdminView.as_view(), name='admin-panel'),

    path('tags/', UserTagListView.as_view(), name='usertag_list'),
    path('tags/<int:pk>/', UserTagDetailView.as_view(), name='usertag_detail'),
    path('tags/create/', UserTagCreateView.as_view(), name='usertag_create'),
    path('tags/<int:pk>/update/', UserTagUpdateView.as_view(), name='usertag_update'),
    path('tags/<int:pk>/delete/', UserTagDeleteView.as_view(), name='usertag_delete'),

    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre_detail'),
    path('genres/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genres/<int:pk>/update/', GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', GenreDeleteView.as_view(), name='genre_delete'),
]