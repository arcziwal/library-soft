from urllib.parse import urlparse
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index-page'),
    path('new_author', views.NewAuthor.as_view(), name='new-author'),
    path('new_publishing_house', views.NewPublishingHouse.as_view(), name='new-publishing-house'),
    path('new_book', views.NewBook.as_view(), name="new-book"),
    path('book/search', views.SearchBook.as_view(), name='search-by-title'),
    path('book/results', views.SearchResults.as_view(), name='search-results'),
    path('book/<int:number>', views.BookDetails.as_view(), name='book-details'),
    path('login/', views.LoginRequest.as_view(), name='login'),
    path('register/', views.CreateUser.as_view(), name='create-user'),
    path('logout/', views.LogoutRequest.as_view(), name='logout'),
]
