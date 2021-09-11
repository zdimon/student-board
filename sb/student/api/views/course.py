from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from student.api.serializers.course import CourseSerializer
from course.models import Course
from student.models import Student2Course

class CourseListView(APIView):
    '''

     Course list.

    '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
    )
    def get(self, request):
        out = []
        for c2s in Student2Course.objects.filter(user=request.user.student):
            out.append(CourseSerializer(c2s.course).data)
        return Response(out)

