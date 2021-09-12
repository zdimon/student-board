from django.urls import path, include
from .views import registration, cabinet, join_course, students

urlpatterns = [ 

    path('registration',registration, name="mentor-registration"),
    path('profile',registration, name="mentor-profile"),
    path('cabinet',cabinet, name="mentor-cabinet"),
    path('join/course/<int:course_id>',join_course, name="join-course-mentor"),
    path('students',students, name="mentor-students"),
]