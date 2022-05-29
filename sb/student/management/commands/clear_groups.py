from django.core.management.base import BaseCommand, CommandError
from course.article_loader import ArticleLoader
from sb.settings import DATA_DIR
from student.models import Exam, ExamQuestion, Student2ExamQuestion, Student, Student2ExamAnswer, StudentGroup
import json
import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Clear groups')
        for group in StudentGroup.objects.all():
            cnt = Student.objects.filter(group=group).count()
            if cnt == 0:
                print('Deleting %s cnt %s' % (group.name, cnt))
                group.delete()
            else:
                print('Leaving %s cnt %s' % (group.name, cnt))
       