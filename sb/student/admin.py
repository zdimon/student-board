from django.contrib import admin
from .models import Student, Student2Kursak, StudentGroup, Student2Course, Student2Lab, StudentPayment, Exam, Student2ExamQuestion, ExamQuestion, Student2ExamAnswer

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['username', 'fname', 'lname', 'group']

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'count']


@admin.register(Student2Course)
class Student2CourseGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Student2Kursak)
class Student2KursakGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Student2Lab)
class Student2LabAdmin(admin.ModelAdmin):
    list_display = ['lab', 'user', 'file', 'gitlink']

@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course','fname','lname','cost','mark', 'type', 'is_done']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'alias', 'date']

@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam']


@admin.register(Student2ExamQuestion)
class Student2ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'user']

@admin.register(Student2ExamAnswer)
class Student2ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'answer']

    