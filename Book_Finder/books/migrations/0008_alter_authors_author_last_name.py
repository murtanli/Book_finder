# Generated by Django 4.0 on 2024-10-15 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_remove_books_book_author_books_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='author_last_name',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
