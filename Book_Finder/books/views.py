from django.db.models import Q
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import *
import json

def main_page(request):
    top_books = Books.objects.filter(rating__gte=4.5).order_by('-rating')[:8]

    books_mas = []
    for book in top_books:
        authors = book.book_author.all()
        image = book.image

        info = {
            'book': book,
            'author': authors,
            'image': image
        }

        books_mas.append(info)

    return render(request, 'main.html', {
        'books_mas': books_mas
    })


def get_book_image(request, image_id):
    image_book = get_object_or_404(ImagesBooks, pk=image_id)
    image_path = image_book.book_cover.path
    return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')


def book_search(request):
    return render(request, 'books_search.html')


def all_authors(request):
    authors = Authors.objects.all()
    authors_list = [{"id": author.id, "name": author.abbreviation} for author in authors]
    return JsonResponse(authors_list, safe=False)

def all_genres(request):
    genres = Genre.objects.all()
    genres_list = [{"id": genre.id, "name": genre.genre_name} for genre in genres]
    return JsonResponse(genres_list, safe=False)

def get_all_books(request):
    books = Books.objects.all()
    books_list = [{
        "id": book.id,
        "book_name": book.book_name,
        "age_limit": book.age_limit,
        "pages": book.pages,
        "genres": [genre.genre_name for genre in book.genres.all()],
        "author_ob": [author.abbreviation for author in book.book_author.all()],
        "description": book.description,
        "image_url": book.image.id,
        "rating": book.rating
    } for book in books]
    return JsonResponse(books_list, safe=False)


def find_book(request):
    if request.method == 'POST':
        authors = json.loads(request.POST.get('authors', '[]'))
        genres = json.loads(request.POST.get('genres', '[]'))
        text = request.POST.get('text')
        print(f"{authors} \n {genres}\n {text}")

        books_query = Books.objects.all()

        if authors:
            books_query = books_query.filter(book_author__abbreviation__in=authors)

        if genres:
            books_query = books_query.filter(genres__genre_name__in=genres)

        if text:
            books_query = books_query.filter(
                Q(book_name__icontains=text) | Q(description__icontains=text)
            )

        books_query = books_query.distinct()

        books_list = [{
            "id": book.id,
            "book_name": book.book_name,
            "age_limit": book.age_limit,
            "pages": book.pages,
            "genres": [genre.genre_name for genre in book.genres.all()],
            "author_ob": [author.abbreviation for author in book.book_author.all()],
            "description": book.description,
            "image_url": book.image.id,
            "rating": book.rating
        } for book in books_query]
        return JsonResponse(books_list, safe=False)