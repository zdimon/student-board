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
        print('Start loading questions %s' % options['alias'])
        try:
            exam = Exam.objects.get(alias=options['alias'])
        except:
            raise Exception('No exam!')
        Student2ExamQuestion.objects.filter(exam=exam).delete()
        Student2ExamAnswer.objects.filter(exam=exam).delete()
        questions = []

        for q in ExamQuestion.objects.filter(exam=exam):
            questions.append(q.id)
        for student in Student.objects.filter(group=exam.group):
            a = Student2ExamAnswer()
            a.user = student
            a.exam = exam
            a.save()
            random.shuffle(questions)
            Student2ExamQuestion.objects.filter(user=student).delete()
            question1 = ExamQuestion.objects.get(pk=questions[0])
            question2 = ExamQuestion.objects.get(pk=questions[1])
            question3 = ExamQuestion.objects.get(pk=questions[2])
            s2q1 = Student2ExamQuestion()
            s2q1.user = student
            s2q1.question = question1
            s2q1.exam = exam
            s2q1.save()

            s2q1 = Student2ExamQuestion()
            s2q1.user = student
            s2q1.question = question2
            s2q1.exam = exam
            s2q1.save()

            s2q1 = Student2ExamQuestion()
            s2q1.user = student
            s2q1.question = question3
            s2q1.exam = exam
            s2q1.save()

            print(student)