from django.urls import path
from .views import CourseListView, KursakListView


urlpatterns = [
    path('kursak/list', KursakListView.as_view()),
    path('course/list', CourseListView.as_view())
]