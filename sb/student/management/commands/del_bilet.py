from django.core.management.base import BaseCommand, CommandError
from course.article_loader import ArticleLoader
from sb.settings import DATA_DIR
from student.models import Exam, ExamQuestion, Student2ExamQuestion, Student, Student2ExamAnswer
import json
import random


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('alias', type=str)

    def handle(self, *args, **options):
        print('Start deleting questions %s' % options['alias'])
        try:
            exam = Exam.objects.get(alias=options['alias'])
        except:
            raise Exception('No exam!')
        Student2ExamQuestion.objects.filter(exam=exam).delete()
        Student2ExamAnswer.objects.filter(exam=exam).delete()
       