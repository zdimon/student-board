from django.contrib import admin

from .models import Mentor2Course, Mentor, Mentor2Group, Mentor2Student, Invitation

# Register your models here.


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    change_form_template = 'loginas/change_form.html'
    list_display = ['username', 'fname', 'lname']

@admin.register(Mentor2Course)
class Mentor2CourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'is_approved']
    list_editable = ['is_approved']

@admin.register(Mentor2Group)
class Mentor2GroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'is_approved']
    list_editable = ['is_approved']

@admin.register(Mentor2Student)
class Mentor2StudentAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'user']

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'group', 'is_approved', 'created_at', 'updated_at']