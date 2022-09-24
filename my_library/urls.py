from urllib.parse import urlparse
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index-page'),
    path('new_author', views.New_author.as_view(), name='new-author'),
]