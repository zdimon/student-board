from django.contrib import admin

from .models import Mentor2Course, Mentor

# Register your models here.


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['username', 'fname', 'lname']

@admin.register(Mentor2Course)
class Mentor2CourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'is_approved']
    list_editable = ['is_approved']
