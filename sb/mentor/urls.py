from django.urls import path, include
from .views import *

urlpatterns = [ 

    path('registration',registration, name="mentor-registration"),
    path('profile',registration, name="mentor-profile"),
    path('cabinet',cabinet, name="mentor-cabinet"),
    path('join/course/<int:course_id>',join_course, name="join-course-mentor"),
    path('students',students, name="mentor-students"),
    path('groups',groups, name="mentor-groups"),
    path('invite', invite, name="invite"),
    path('courses',courses, name="mentor-courses"),
    path('course-detail/<int:course_id>',course_detail, name="mentor-course-detail"),
    path('notify/<int:lesson_id>',notify, name="mentor-notify"),
]