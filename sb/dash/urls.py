from django.urls import path, include
from .views import index, login, logout, courses


urlpatterns = [ 
   path('login',login, name="login"),
   path('logout',logout, name="logout"),
   path('',index, name="index"),
   path('courses',courses, name="courses"),
]