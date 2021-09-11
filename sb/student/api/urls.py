from django.urls import path
from .views import CourseListView


urlpatterns = [
    path('course/list', CourseListView.as_view())
]