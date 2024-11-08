from django.db import models


class Authors(models.Model):
    gender_choices = [
        ('Ж', 'Женский'),
        ('М', 'Мужской'),
        ('Н', 'Неизвестен'),
    ]

    author_first_name = models.CharField(max_length=15)
    author_last_name = models.CharField(max_length=15, null=True, blank=True)
    author_surname = models.CharField(max_length=15, null=True, blank=True)
    abbreviation = models.CharField(max_length=25)
    rating = models.FloatField(default=0.0)
    gender = models.CharField(max_length=1, choices=gender_choices)

    def __str__(self):
        return f"{self.author_first_name} {self.author_last_name}"


class Genre(models.Model):
    genre_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genre_name


class ImagesBooks(models.Model):
    book_cover = models.ImageField(upload_to='Book_covers/', blank=True)

    def __str__(self):
        return self.book_cover.name if self.book_cover else 'No cover'


class Books(models.Model):
    book_name = models.CharField(max_length=50)
    age_limit = models.IntegerField(default=0)
    pages = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    book_author = models.ManyToManyField(Authors)
    description = models.TextField()
    image = models.ForeignKey(ImagesBooks, models.CASCADE)
    rating = models.FloatField(default=0.0)
