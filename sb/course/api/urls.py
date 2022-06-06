from django.urls import path
from .views import IsCoursePaidview


urlpatterns = [
    path('is_course_paid/<int:course_id>', IsCoursePaidview.as_view()),
]