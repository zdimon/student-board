from django.core.management.base import BaseCommand, CommandError
from course.models import Course, Topic, Lesson
from course.course_loader import CourseLoader
from sb.settings import DATA_DIR
import subprocess
from course.models import Kursak
from django.core.files import File
import fitz



class Command(BaseCommand):

    def add_arguments(self, parser):
       parser.add_argument('-l', '--lesson', type=str, help='Lesson id', )
    
    def handle(self, *args, **options):
        print('Start loading topics from %s' % DATA_DIR)
        if(options['lesson']):
            lesson = Lesson.objects.get(pk=int(options['lesson']))
            arrf = []
            titles = []
            for t in Topic.objects.filter(lesson=lesson):
                titles.append(t.title)
                less = lesson.name_slug.split('--')
                l = less[1]
                pathmd = f'{DATA_DIR}/{lesson.course.name_slug}/{l}/{t.filename}'
                
                
                pathpdf = f'{DATA_DIR}/{lesson.course.name_slug}/{less[1]}/{t.id}.pdf'
                print(pathmd)
                bashCommand = f'md2pdf {pathmd}'
                print(bashCommand)
                arrf.append(pathpdf)

                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                result = fitz.open()

            print(arrf)
            outp = f'{DATA_DIR}/{lesson.course.name_slug}/{less[1]}/kursak.pdf'
            for pdf in arrf:
                with fitz.open(pdf) as mfile:
                    result.insertPDF(mfile)
                
            result.save(outp)

            try:
                k = Kursak.objects.get(name_slug=t.id)
            except:
                k = Kursak()
                k.course = lesson.course
                k.title = ' '.join(titles)
                k.save()
                with open(outp,'rb') as img_file:
                    k.file.save('test.pdf', File(img_file), save=True)
                print('Saving kursak')