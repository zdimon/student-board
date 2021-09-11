from django.core.management.base import BaseCommand, CommandError
from course.models import Course
from course.course_loader import CourseLoader
from sb.settings import DATA_DIR

class Command(BaseCommand):

    def add_arguments(self, parser):
       parser.add_argument('-c', '--course', type=str, help='Course name', )
    
    def handle(self, *args, **options):
        print('Start loading courses from %s' % DATA_DIR)
        if(options['course']):
            loader = CourseLoader(options['course'])
            loader.process()
        else:
            for d in CourseLoader.get_active_courses_dirs():
                loader = CourseLoader(d)
                loader.process()