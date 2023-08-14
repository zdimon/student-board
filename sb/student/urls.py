from django.urls import path, include
from .views import profile, registration, cabinet, join_course, detail_course, detail_lesson, labs, replanish, detail_lab, delete_lab, user_login, detail_kursak, exam_pass, mygroup, invite, newlesson, paylesson, pay_course, pay_course_button, pay_course_test,pay_course_from_account, paid_lesson, paid_course

urlpatterns = [ 
    path('user-login',user_login, name="user-login"),
    path('profile',profile, name="student-profile"),
    path('registration',registration, name="student-registration"),
    path('cabinet',cabinet, name="student-cabinet"),
    path('mygroup',mygroup, name="student-mygroup"),
    path('join/course/<int:course_id>',join_course, name="join-course-student"),
    path('detail/course/<str:course_name_slug>',detail_course, name="detail-course-student"),
    path('detail/lesson/<int:lesson_id>',detail_lesson, name="detail-lesson-student"),
    path('labs',labs, name="student-labs"),
    path('labs/<int:course_id>',labs, name="student-course-labs"),
    path('replanish',replanish, name="replanish"),
    path('detail/lab/<int:lab_id>',detail_lab, name="detail-lab-student"),
    path('delete/lab/<int:lab_id>',delete_lab, name="delete-lab-student"), 
    path('detail/kursak/<int:kursak_id>',detail_kursak, name="detail-kursak-student"), 
    path('exampass/<int:exam_id>',exam_pass, name="exam-pass-student"),
    path('invite/<str:uuid>', invite, name="student-invite"),
    path('newlesson/<str:uuid>/<int:lesson_id>', newlesson, name="student-newlesson"),
    path('paylesson/<int:lesson_id>', paylesson, name="student-paylesson"),
    path('pay_course/<str:course_id>', pay_course, name="pay-course"),
    path('pay_course_button/<int:payment_id>', pay_course_button, name="pay-course-button"),
    path('pay_course_test/<int:course_id>', pay_course_test, name="pay-course-test"),
    path('pay_course_from_account/<int:course_id>', pay_course_from_account, name="pay-course-from-account"),

    path('paidcourse/<str:uuid>/<str:course_id>', paid_course, name="paid_course"),

    path('paidlesson/<str:uuid>/<str:lesson_id>', paid_lesson, name="paid_lesson"),

]

