from django.core.management.base import BaseCommand, CommandError
from course.models import Course, Lesson, Topic, LessonPayments
from course.course_loader import CourseLoader
from pl.settings import DATA_DIR

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Clearing  DB')
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Topic.objects.all().delete()