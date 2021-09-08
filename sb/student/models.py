from django.db import models
from django.contrib.auth.models import User


class Student(User):
    fname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='student_images')
    account = models.IntegerField()
    phone = models.CharField(max_length=100)

