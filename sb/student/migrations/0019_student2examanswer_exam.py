# Generated by Django 3.0.7 on 2022-05-24 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_student2examanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='student2examanswer',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Exam'),
        ),
    ]
