from django.db import models
from django.contrib.auth.models import User
from course.models import Course, Lab, Kursak
from django.utils.translation import ugettext as _

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

class Student2Lab(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab,on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True, help_text=_('Text answer. For example your source code.'))
    gitlink = models.CharField(max_length=250, help_text=_('Link to the git repo'))
    file = models.FileField(upload_to="labs", help_text=_('File or zip archive'), null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    mark = models.IntegerField(default=0)

class StudentPayment(models.Model):

    TYPE_CHOICES = (
        ("course", "course"),
        ("kursak", "kursak"),
    )
    type = models.CharField(max_length=9,
                  choices=TYPE_CHOICES,
                  default="course")
    user = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True,blank=True)
    kursak = models.ForeignKey(Kursak,on_delete=models.SET_NULL,null=True,blank=True)
    is_done = models.BooleanField(default=False)

    mark = models.CharField(max_length=50,null=True,blank=True)
    fname = models.CharField(max_length=250,null=True,blank=True)
    lname = models.CharField(max_length=250,null=True,blank=True)
    sname = models.CharField(max_length=250,null=True,blank=True)
    group = models.CharField(max_length=250,null=True,blank=True)
    cost = models.IntegerField()
    email = models.CharField(max_length=250,null=True,blank=True)

