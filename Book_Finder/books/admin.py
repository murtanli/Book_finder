
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Authors, Genre, ImagesBooks, Books

@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('id','author_first_name', 'author_last_name', 'author_surname', 'abbreviation', 'rating', 'gender')
    search_fields = ('id','author_first_name', 'author_last_name', 'abbreviation')
    list_filter = ('gender',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id','genre_name',)
    search_fields = ('id','genre_name',)

@admin.register(ImagesBooks)
class ImagesBooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview',)
    search_fields = ('id','book_cover',)
    def image_preview(self, obj):
        if obj.book_cover:
            image_id = obj.id
            url = reverse('get_book_image', args=[image_id])
            return format_html('<img src="{}" alt="Image" style="max-width: 200px; max-height: 100px;" />', url)
        return None

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id','book_name', 'book_genres', 'book_authors', 'age_limit', 'pages', 'image_preview', 'description', 'rating')
    search_fields = ('id','book_name', 'description')
    list_filter = ('genres', 'book_author')

    def image_preview(self, obj):
        if obj.image:
            image_id = obj.image.id
            url = reverse('get_book_image', args=[image_id])
            return format_html('<img src="{}" alt="Image" style="max-width: 200px; max-height: 100px;" />', url)
        return None

    def book_authors(self, obj):
        authors = obj.book_author.all()
        return ", ".join([f"{author.author_first_name} {author.author_last_name} " for author in authors])

    def book_genres(self, obj):
        genres = obj.genres.all()
        return ", ".join([f"{genre.genre_name}" for genre in genres])

