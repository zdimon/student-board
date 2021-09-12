from django.urls import path, include
from .views import index, login, logout, courses, set_lang


urlpatterns = [ 
   path('login',login, name="login"),
   path('logout',logout, name="logout"),
   path('',index, name="index"),
   path('courses',courses, name="courses"),
   path('sel_lang/<str:lang>',set_lang, name="set-lang"),
]