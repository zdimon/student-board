from django.contrib import admin
from .models import Student, Student2Kursak, StudentGroup, Student2Course, Student2Lab, StudentPayment, Exam, Student2ExamQuestion, ExamQuestion, Student2ExamAnswer, EmailTemplate, StudentGroup2Course, LessonPayment, Replanishment, CoursePayment

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ['username', 'surname', 'fname', 'lname', 'group', 'account']
    list_editable = ['account']

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

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'alias']
    
@admin.register(StudentGroup2Course)
class StudentGroup2CourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'group']

@admin.register(LessonPayment)
class LessonPaymentAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user']


@admin.register(CoursePayment)
class CoursePaymentAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'is_approved']
    list_editable = ['is_approved']

@admin.register(Replanishment)
class ReplanishmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'ammount', 'is_approved']
