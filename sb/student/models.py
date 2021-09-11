from django.db import models
from django.contrib.auth.models import User
from course.models import Course

class StudentGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(User):
    fname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='student_images')
    account = models.IntegerField(default=0)
    phone = models.CharField(max_length=100)
    group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return '/static/img/user.svg'


class Student2Course(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)