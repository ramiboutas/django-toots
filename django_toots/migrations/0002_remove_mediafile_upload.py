# Generated by Django 4.2.4 on 2023-08-28 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_tweets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediafile',
            name='upload',
        ),
    ]
