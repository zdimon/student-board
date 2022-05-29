from django.db import models
from django.contrib.auth.models import User
from course.models import Course
from student.models import Student, StudentGroup
import uuid

class Mentor(User):
    fname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='student_images')
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return '/static/img/user.svg'


class Mentor2Course(models.Model):
    user = models.ForeignKey(Mentor,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

class Mentor2Group(models.Model):
    group = models.ForeignKey(StudentGroup,on_delete=models.CASCADE)
    user = models.ForeignKey(Mentor,on_delete=models.CASCADE, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

class Mentor2Student(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor,on_delete=models.CASCADE)

class Invitation(models.Model):
    email = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    group = models.ForeignKey(StudentGroup,on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
