# Generated by Django 4.0 on 2024-10-15 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_authors_author_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='book_author',
        ),
        migrations.AddField(
            model_name='books',
            name='book_author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='books.authors'),
            preserve_default=False,
        ),
    ]
