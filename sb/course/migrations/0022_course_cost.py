# Generated by Django 3.0.7 on 2022-06-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_kursak_name_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cost',
            field=models.IntegerField(default=0),
        ),
    ]
