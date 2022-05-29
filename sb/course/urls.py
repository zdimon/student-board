from django.urls import path, include
from course.views import course_detail, lesson_detail, pay, my_cabinet, save_comment, discussion, subscribe, unsubscribe
from course.views import articles
from course.views import article_detail, pay_success, comment_detail, sitemap, show_tag

urlpatterns = [ 
    path('detail/<slug:slug>',course_detail, name="course_detail"),
    path('lesson/detail/<slug:slug>',lesson_detail, name="lesson_detail"),
    path('pay/<int:lesson_id>',pay, name="pay"),
    path('my/cabinet',my_cabinet, name="my_cabinet"),
    path('save/comment',save_comment, name="save_comment"),
    path('discussion',discussion, name="discussion"),
    path('subscribe',subscribe, name="subscribe"),

    path('unsubscribe',unsubscribe, name="unsubscribe"),

    path('articles',articles, name="articles"),
    path('article/<slug:slug>',article_detail, name="article_detail"),
    path('pay/success/<int:lesson_id>',pay_success, name="pay_success"),

    path('comment/detail/<int:id>',comment_detail, name="comment_detail"),
    path('map',sitemap, name="map"),

    path('tag/<slug:tag>',show_tag, name="show-tag"),

]