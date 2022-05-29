# Generated by Django 3.0.7 on 2021-10-23 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_kursak_name_slug'),
        ('student', '0012_studentpayment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student2Kursak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kursak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Kursak')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
    ]
