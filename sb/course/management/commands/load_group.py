from django.core.management.base import BaseCommand, CommandError
from course.models import Course, Lesson, Topic, LessonPayments
from course.course_loader import CourseLoader
from student.models import StudentGroup

num_ears = [1,2,3,4,5,6]
num_order = [1,2]


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Loading groups')
        StudentGroup.objects.all().delete()
        for y in num_ears:
            StudentGroup.objects.create(
                name = '%sПР1'  % y
            )
            StudentGroup.objects.create(
                name = '%sПРC'  % y
            )
            StudentGroup.objects.create(
                name = '%sПР2' % y
            )


