# Generated by Django 3.0.7 on 2022-05-28 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentor', '0006_mentor2student'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
