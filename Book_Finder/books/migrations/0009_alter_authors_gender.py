# Generated by Django 4.0 on 2024-10-15 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_authors_author_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женский'), ('М', 'Мужской'), ('Н', 'Неизвестен')], max_length=1),
        ),
    ]
