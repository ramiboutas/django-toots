# Generated by Django 4.2.4 on 2023-09-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_toots", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tootfile",
            name="expires_at",
        ),
        migrations.RemoveField(
            model_name="tootfile",
            name="media_id_string",
        ),
        migrations.AddField(
            model_name="tootfile",
            name="url",
            field=models.URLField(blank=True, editable=False, null=True),
        ),
    ]
