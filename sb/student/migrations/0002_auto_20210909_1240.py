# Generated by Django 3.0.7 on 2021-09-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='account',
            field=models.IntegerField(default=0),
        ),
    ]
