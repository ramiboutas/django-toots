# Generated by Django 4.2.4 on 2023-08-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_djangonewsissue_issue_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='djangonewsissue',
            name='issue_url',
            field=models.URLField(null=True),
        ),
    ]
