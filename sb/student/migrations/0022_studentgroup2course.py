# Generated by Django 3.0.7 on 2022-05-28 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_kursak_name_slug'),
        ('student', '0021_student_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup2Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.StudentGroup')),
            ],
        ),
    ]
