from rest_framework import serializers
from course.models import Course, Kursak


class KursakSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Kursak
        fields = [
            'id',
            'title'
        ]