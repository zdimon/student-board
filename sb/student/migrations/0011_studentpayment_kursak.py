# Generated by Django 3.0.7 on 2021-10-23 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_kursak_name_slug'),
        ('student', '0010_auto_20211022_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentpayment',
            name='kursak',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='course.Kursak'),
        ),
    ]
