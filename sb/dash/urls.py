from django.urls import path, include
from .views import index, login, logout, courses, set_lang, buy_course, pay_success, pay_process, prepay, oferta, delivery, confident, about, pay_kursak


urlpatterns = [ 
   path('about',about, name="about"),
   path('oferta',oferta, name="oferta"),
   path('delivery',delivery, name="delivery"),
   path('confident',confident, name="confident"),
   path('login',login, name="login"),
   path('logout',logout, name="logout"),
   path('',index, name="index"),
   path('courses',courses, name="courses"),
   path('sel_lang/<str:lang>',set_lang, name="set-lang"),
   path('buy/course/<int:order_id>',buy_course, name="buy-course"),
   path('pay/success',pay_success, name="pay-success"),
   path('pay/process',pay_process, name="pay-process"),
   path('prepay/<int:course_id>',prepay, name="prepay"),
   path('pay/kursak/<int:kursak_id>',pay_kursak, name="pay-kursak"),
]