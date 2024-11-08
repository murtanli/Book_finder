import os
import django
import re
import requests
import sys

from Author_parse import Author_parse
from django.core.files.base import ContentFile

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bs4 import BeautifulSoup as bs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Book_Finder.settings')
django.setup()

from books.models import *


class Book_parser:

    def __init__(self):
        self.page = None
        self.url = "https://litlife.club/popular_books/year?page="
        self.soup = None

    def fetch_page(self):
        response = requests.get(f'{self.url}{self.page}')
        self.soup = bs(response.content, 'html.parser')

    def save_cover_book(self, book):

        book_img_block = book.find('img')

        if book_img_block:
            book_img_src = None

            if 'src' in book_img_block.attrs and book_img_block['src']:
                book_img_src = book_img_block['src']
            elif 'data-src' in book_img_block.attrs:
                book_img_src = book_img_block['data-src']
            elif 'data-srcset' in book_img_block.attrs:
                book_img_src = book_img_block['data-srcset']
            if book_img_src and book_img_src.startswith('//'):
                book_img_src = 'https:' + book_img_src

            response = requests.get(book_img_src)

            if response.status_code == 200:
                image_name = book_img_src.split('/')[-1]
                image_book = ImagesBooks.objects.create(book_cover=None)
                image_book.book_cover.save(image_name, ContentFile(response.content), save=True)
                return image_book.id
            else:
                print("Error get photo")

    def save_genres(self, genre):
        find_genre = Genre.objects.filter(genre_name=genre).first()
        if not find_genre:
            new_genre = Genre.objects.create(genre_name=genre)
            return new_genre.id
        else:
            return find_genre.id

    def save_author(self, author_inf, full_name):
        mas_ids = []
        for i in range(len(full_name)):
            full_name_split = full_name[i].split(' ')
            full_name_split = [name for name in full_name_split if name]
            find_author = None
            abbreviation = ""
            first_name = last_name = surname = None


            if len(full_name_split) == 1:
                first_name = full_name_split[0]
                find_author = Authors.objects.filter(author_first_name=first_name).first()
                abbreviation = first_name
                print(abbreviation)

            if len(full_name_split) == 2:
                first_name = full_name_split[1]
                last_name = full_name_split[0]
                find_author = Authors.objects.filter(author_first_name=first_name, author_last_name=last_name).first()
                abbreviation = f'{last_name} {first_name[0]}'
                print(abbreviation)

            elif len(full_name_split) == 3:
                first_name = full_name_split[1]
                last_name = full_name_split[0]
                surname = full_name_split[2]
                find_author = Authors.objects.filter(author_first_name=first_name, author_last_name=last_name,
                                                     author_surname=surname).first()
                abbreviation = f'{last_name} {first_name[0]} {surname[0]}'

            if not find_author:
                gender = author_inf[i].get('gender', None)
                if gender:
                    gender = gender[0].upper()

                new_author = Authors.objects.create(
                    author_first_name=first_name,
                    author_last_name=last_name if last_name else None,
                    author_surname=surname if surname else None,
                    abbreviation=abbreviation,
                    rating=author_inf[i].get('rating', None),
                    gender=gender
                )
                print(f"Создан новый автор: {new_author}")
                mas_ids.append(new_author.id)
            else:
                mas_ids.append(find_author.id)
        return mas_ids

    def save_book(self, book_name, age_limit, pages, genres, book_author, description, image, rating):
        if book_name and pages and genres and book_author and description and image and rating:

            image_instance = ImagesBooks.objects.filter(id=image).first()

            if image_instance is None:
                print(f"Изображение с ID {image} не существует.")
                return
            if age_limit is None:
                age_limit = 0
            new_book = Books.objects.create(
                book_name=book_name,
                age_limit=age_limit,
                pages=pages,
                description=description,
                image=image_instance,
                rating=rating
            )
            author_instances = []
            for author in book_author:
                author_instance = Authors.objects.filter(id=author).first()
                if author_instance:
                    author_instances.append(author_instance)
            new_book.book_author.set(author_instances)

            genre_instances = []
            for genre in genres:
                genre_instance = Genre.objects.filter(id=genre).first()
                if genre_instance:
                    genre_instances.append(genre_instance)
            new_book.genres.set(genre_instances)


            print(f"|{'_' * 20}|"
                  f"\nНазвание книги: {book_name}"
                  f"\nВозрастное ограничение: {age_limit}"
                  f"\nКоличество страниц: {pages}"
                  f"\nЖанры: {', '.join([g.genre_name for g in genre_instances])}"
                  f"\nАвтор: {book_author}"
                  f"\nОписание: {description}"
                  f"\nРейтинг: {rating}"
                  f"\n|{'_' * 20}|")

    def parse_books(self):
        books = self.soup.find_all('div', class_='card-body')
        book_name = age_limit = pages = genres = book_author = description = image = rating = None

        for book in books:
            genre_id = []

            image = self.save_cover_book(book)

            # возраст
            age_limit = book.find('sup')
            if age_limit is not None:
                age_limit = age_limit.text.replace('+', '')

            block_col_12 = book.select('div.col-12:not([class*=" "])')

            # Страницы, жанры, авторы, описание и рейтинг книги
            for block in block_col_12:
                pattern_genres = r'(Жанр(?:ы)?:)\s*((?:<a.*?>.*?</a>\s*,?\s*)+)'
                match_genres = re.search(pattern_genres, str(block))
                if match_genres:
                    genres_html = match_genres.group(2)
                    pattern_links = r'<a.*?>(.*?)</a>'
                    genres = re.findall(pattern_links, genres_html)
                    for genre in genres: genre_id.append(self.save_genres(genre))

                    genres = genre_id

                pattern_pages = r'Страниц:\s*(\d+)'
                match_pages = re.search(pattern_pages, str(block))
                if match_pages:
                    pages = match_pages.group(1)

                author_block = block.find_all('a', class_='author name')

                mas_authors_inf = []
                mas_authors_names = []
                for author in author_block:
                    author_parse = Author_parse(author['href'])
                    author_inf = author_parse.parse_info()

                    mas_authors_names.append(author.text.strip())
                    mas_authors_inf.append(author_inf)

                book_author = self.save_author(mas_authors_inf, mas_authors_names)

                desc_block = block.find('div', class_='mt-3')
                description = desc_block.text.strip().replace('далее', '')

                pattern_rating = f'Оценка:\s*(\d+...)'
                match_rating = re.search(pattern_rating, str(block))
                if match_rating:
                    rating = match_rating.group(1)

            # Название книги
            title_block = book.find('h3', class_='break-word h5')
            if title_block:
                book_name = title_block.find('a').text.strip()

            self.save_book(book_name, age_limit, pages, genres, book_author, description, image, rating)

    def run(self):
        Authors.objects.all().delete()
        Genre.objects.all().delete()
        ImagesBooks.objects.all().delete()
        Books.objects.all().delete()
        for i in range(2):
            self.page = i + 1
            self.fetch_page()
            self.parse_books()

        print(f"\n \n Сохранено {self.page} страниц")


if __name__ == "__main__":
    parser = Book_parser()
    parser.run()
