import os
import django
import re
import requests
import sys

from django.core.files.base import ContentFile

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bs4 import BeautifulSoup as bs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Book_Finder.settings')
django.setup()

from books.models import *


class Author_parse:
    def __init__(self, author_url):
        self.author_url = author_url
        response = requests.get(self.author_url)
        self.soup = bs(response.content, 'html.parser')

    def parse_info(self):
        about_author = self.soup.find_all('div', class_='row')
        author_info = {}
        if about_author:
            for block in about_author:
                block_gender = block.find_all('div', class_='col-12 text-wrap')

                for block_gen in block_gender:
                    text_block = block_gen.get_text(separator=' ', strip=True)
                    if 'Пол:' in text_block:
                        pattern_gender = r'Пол:\s*(мужской|женский|неизвестен)'
                        gender = re.search(pattern_gender, text_block)
                        if gender:
                            author_info['gender'] = gender.group(1)
                    elif 'Средняя оценка:' in text_block:
                        pattern_rating = r'Средняя оценка:\s*([\d\.]+)'
                        rating = re.search(pattern_rating, text_block)
                        if rating:
                            author_info['rating'] = rating.group(1)
        return author_info

