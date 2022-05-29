# Generated by Django 3.0.7 on 2022-05-28 21:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_studentgroup2course'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
