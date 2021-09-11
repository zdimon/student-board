from django.urls import path, include
from .views import registration, cabinet

urlpatterns = [ 

    path('registration',registration, name="mentor-registration"),
    path('profile',registration, name="mentor-profile"),
    path('cabinet',cabinet, name="mentor-cabinet"),
]