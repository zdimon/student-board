from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from course.models import Course
from rest_framework.exceptions import APIException

class IsCoursePaidview(APIView):
    '''

     Check if the course paid.

    '''
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema()
    def get(self, request, course_id):
        out = {"is_paid": False}
        try:
            student = request.user.student
        except:
            raise APIException('Student not found!')
        try:
            course = Course.objects.get(pk=course_id)
        except:
            raise APIException('Couse not found!')
        is_paid = Course.is_course_paid(student, course)
        out['is_paid'] = is_paid
        return Response(out)

