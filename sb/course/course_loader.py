from course.models import  Course, Lesson, Topic, Lab
from sb.settings import DATA_DIR, VIDEO_DIR
from os import listdir
from os.path import isfile, join, isdir
import sys
from tagging.models import Tag

import yaml
from django.core.files import File

def save_lab(lesson,variants):
    print('Saving lab')
    try:
        lab = Lab.objects.get(lesson=lesson)
    except:
        lab = Lab()
        lab.lesson = lesson
        lab.course = lesson.course
        lab.title = 'Лабораторная работа #%s' % lesson.number
    lab.variants = variants
    lab.save()


class CourseLoader(object):

    def __init__(self, *args, **kwargs):
        self.dir = args[0]

   
    def process(self):
        self.get_course_or_create()
        self.save_meta_course()
        self.save_lessons()


    def save_meta_course(self):
        path = DATA_DIR+'/'+self.dir+'/meta.yml'
        print('Saving meta for %s' % self.course.name_slug)
        meta = self.get_meta(path)
        self.course.name = meta['title']
        self.course.meta_keywords = meta['meta_keywords']
        self.course.meta_title = meta['meta_title']
        self.course.meta_description = meta['meta_description']
        self.course.desc = meta['desc']
        self.course.save()
        try:
            im_path = DATA_DIR+'/'+self.dir+'/image.png'
            print('Loading image %s' % im_path)
            with open(im_path,'rb') as img_file:
                self.course.image.save('image.png', File(img_file), save=True)
        except Exception as e:
            print(str(e))

    def get_course_or_create(self):
        try: 
            self.course = Course.objects.get(name_slug=self.dir)
        except:
            self.course = Course()
            self.course.name_slug = self.dir
            self.course.save()

    def get_meta(self,path):
        if isfile(path):
            f = open(path,'r')
            str = f.read()
            f.close()
            yml = yaml.load(str, Loader=yaml.FullLoader)
            return yml
        else:
            return False

    def save_lessons(self):
        path = DATA_DIR+'/'+self.dir
        onlydirs = [f for f in listdir(path) if isdir(join(path, f))]
        for d in onlydirs:
            if d != 'code':
                lesson_yml_path = path+'/'+d+'/meta.yml'
                data = self.get_meta(lesson_yml_path)
                slug = '%s--%s' % (self.course.name_slug, d)
                try:
                    lesson = Lesson.objects.get(name_slug=slug)
                except:
                    lesson = Lesson()
                number = d.split('-')[0]
                
                lesson.name_slug = slug
                lesson.number = number 
                try:
                    lesson.title = data['name']
                except:
                    lesson.title = 'Не определено!'
                    print('Ошибка в %s' % lesson_yml_path)
                    sys.exit()
                try:
                    lesson.desc = data['desc']
                except:
                    print('Error with desc in %s' % lesson_yml_path)

                try:
                    lesson.created_at = data['created']
                except:
                    lesson.created_at = '2000-01-01'

                lesson.meta_keywords = data['meta_keywords']
                lesson.meta_title = data['meta_title']
                lesson.meta_description = data['meta_description']
                lesson.course = self.course
                lesson.save()
                ## add tags
                if 'tags' in data:
                    tags = data['tags'].split(' ')
                    for tag in tags:
                        Tag.objects.add_tag(lesson, tag)
                print('Saving lesson...%s' % data['slug'])
                for f in data['files']:
                    if f['file'] == 'lab.md':
                        save_lab(lesson,f['variants'])
                        continue
                    try:
                        topic = Topic.objects.get(lesson=lesson,filename=f['file'])
                    except Exception as e:
                        topic = Topic.objects.create(filename=f['file'], course=self.course, title=f['title'], lesson=lesson, created_at='2000-01-01')
                    ## make order
                    try:
                        order = f['order']
                        topic.order = order
                        topic.save()
                    except:
                        pass

                    try:
                        order = f['created']
                        topic.created_at = f['created']
                        topic.save()
                    except:
                        pass

                    print('Saving topic %s' % f['file'])
                    topic.check_video(f)

    @staticmethod
    def get_active_courses_dirs():
        out = []
        onlydirs = [f for f in listdir(DATA_DIR) if isdir(join(DATA_DIR, f))]
        for d in onlydirs:
            if d.find('.') == -1 and d != 'articles' and d != 'kursak':
                out.append(d)
        return out


