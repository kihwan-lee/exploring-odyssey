# Generated by Django 3.1.2 on 2020-11-13 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_article_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='city',
        ),
        migrations.RemoveField(
            model_name='author',
            name='city',
        ),
    ]