from django.db import models
from django.contrib.auth.models import User
from course.models import Course
from student.models import StudentGroup


class Mentor(User):
    fname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='student_images')
    phone = models.CharField(max_length=100)


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