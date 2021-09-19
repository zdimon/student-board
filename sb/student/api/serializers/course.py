from rest_framework import serializers
from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'desc',
            'image_url',
            'get_student_absolute_url'
        ]