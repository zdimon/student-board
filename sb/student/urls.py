from django.urls import path, include
from .views import profile, registration, cabinet, join_course, detail_course, detail_lesson

urlpatterns = [ 
    path('profile',profile, name="student-profile"),
    path('registration',registration, name="student-registration"),
    path('cabinet',cabinet, name="student-cabinet"),
    path('join/course/<int:course_id>',join_course, name="join-course-student"),
    path('detail/course/<int:course_id>',detail_course, name="detail-course-student"),
    path('detail/lesson/<int:lesson_id>',detail_lesson, name="detail-lesson-student"),
]