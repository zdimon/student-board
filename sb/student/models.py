from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from course.models import Course, Lab, Kursak, Lesson
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
import uuid
class EmailTemplate(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    alias = models.CharField(max_length=50)

class StudentGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    @property
    def count(self):
        return Student.objects.filter(group=self).count()


class Student(User):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    fname = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='student_images')
    account = models.IntegerField(default=100)
    phone = models.CharField(max_length=100)
    group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def full_name(self):
        return '%s %s %s' % (self.surname, self.fname, self.lname)

    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return '/static/img/user.svg'
            
    @property
    def get_exam_link(self):
        try:
            exam = Exam.objects.get(group=self.group)
        except:
            return _('Экзамена нет')
        links = []
        for a in Student2ExamAnswer.objects.filter(exam=exam, user=self):
            
            if a.answer:
                links.append('<a target=_blank href="%s" >%s</a>' % (a.answer.url,"Ответ"))
            else:
                links.append('<span style="color: red">Ответа нет</span>')
        out = '</br>'.join(links)
        return mark_safe(out)



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

class Student2Kursak(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    kursak = models.ForeignKey(Kursak,on_delete=models.CASCADE)
    

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

    def make_payment(self):
        from student.models import Student2Kursak, Student2Course
        self.is_done = True
        self.save()
        if self.type == 'kursak':
            try:
                s2k = Student2Kursak.objects.get(user=self.user,kursak=self.kursak)
            except:
                s2k = Student2Kursak()
                s2k.user = self.user
                s2k.kursak = self.kursak
                s2k.save()

        if self.type == 'course':
            try:
                s2k = Student2Course.objects.get(user=self.user,course=self.course)
            except:
                s2c = Student2Course()
                s2c.user = self.user
                s2c.course = self.course
                s2c.save()

class Exam(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    alias = models.CharField(max_length=250, blank=True, verbose_name=_(u'Alias'))
    date = models.DateTimeField()
    group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        return self.name

class ExamQuestion(models.Model):
    text = models.TextField(max_length=250, blank=True, verbose_name=_(u'Text'))
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True) 

    def __str__(self):
        return self.text


class Student2ExamQuestion(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    question = models.ForeignKey(ExamQuestion,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE, null=True, blank=True)

class Student2ExamAnswer(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    answer = models.FileField(upload_to="exam_answer", null=True, blank=True)
    exam = models.ForeignKey(Exam,on_delete=models.SET_NULL, null=True, blank=True)

class StudentGroup2Course(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup,on_delete=models.CASCADE)

class LessonPayment(models.Model):
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)