from django.core.management.base import BaseCommand, CommandError
from course.article_loader import ArticleLoader
from sb.settings import DATA_DIR
from student.models import Exam, ExamQuestion
import json


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('alias', type=str)

    def handle(self, *args, **options):
        print('Start loading questions %s/%s' % (DATA_DIR, options['alias']))
        try:
            exam = Exam.objects.get(alias=options['alias'])
        except:
            raise Exception('No exam!')
        ExamQuestion.objects.filter(exam=exam).delete()
        path = '%s/%s/questions.json' % (DATA_DIR, options['alias'])
        fl = open(path,'r')
        txt = fl.read()
        fl.close()
        json_data = json.loads(txt)
        for i in json_data:
            print(i)
            q = ExamQuestion()
            q.text = i
            q.exam = exam
            q.save()
        #for d in ArticleLoader.get_active_catalog_dirs():
        #    loader = ArticleLoader(d)
        #    loader.process()