from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name="main_page"),
    path('get_book_image/<int:image_id>/', get_book_image, name='get_book_image'),
    path('search_book/', book_search, name="search_book"),
    path('get_all_authors/', all_authors, name="all_authors"),
    path('get_all_genres/', all_genres, name="all_genres"),
    path('get_all_books/', get_all_books, name="get_all_books"),
    path('find_book/', find_book, name="find_book"),
]