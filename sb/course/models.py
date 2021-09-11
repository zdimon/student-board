from django.db import models
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.urls import reverse
from sb.settings import DATA_DIR, ALL_FREE, VIDEO_DIR
import os
from tagging.registry import register
from tagging.models import Tag



import markdown
from os.path import isfile, join, isdir
from os import listdir

from bs4 import BeautifulSoup


def parse_md(txt):
    try:
        txt = txt.decode('UTF-8')
    except:
        pass
    return mark_safe(markdown.markdown(txt,extensions=['extra', 'smarty'], output_format='html5'))


class Course(models.Model):
    name = models.CharField(max_length=250, verbose_name=_(u'Name'), blank=True, null = True)
    desc = models.TextField(verbose_name=_(u'Description'), blank=True, null = True)
    image = models.ImageField(verbose_name=_(u'Image'), upload_to='course_images', blank=True, null = True)
    meta_keywords = models.TextField(blank=True, null = True)
    meta_title = models.CharField(max_length=255, blank=True, null = True)
    meta_description = models.TextField(blank=True, null = True)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True, null = True)
    is_active = models.BooleanField(verbose_name=_('Is published?'), default=False)
    order = models.IntegerField(default=0)

    @property
    def lessons(self):
        return Lesson.objects.filter(course=self).order_by('number');
    @property
    def count_lessons(self):
        return Lesson.objects.filter(course=self).count()

    @property
    def mentors(self):
        from mentor.models import Mentor2Course
        mts = Mentor2Course.objects.filter(course=self)
        out = ''
        for m in mts:
            out = out + ' ' + '%s %s %s' % (m.user.fname, m.user.lname, m.user.surname)
        return out

    @property
    def get_last_lessons(self):
        return Lesson.objects.filter(course=self).order_by('-number')[0:2]


    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.name_slug })

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return self.image.url

    @property
    def image_tag(self):
        return mark_safe('<img width="60" src="%s" />' % self.image.url)

class Lesson(models.Model):
    title = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    number = models.IntegerField(default=0, verbose_name=_(u'Number'))
    is_active = models.BooleanField(verbose_name=_('Is active?'), default=False)
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='lessons_images', null = True)
    course = models.ForeignKey(Course, verbose_name=_(u'Course'), on_delete=models.CASCADE)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    desc = models.TextField(verbose_name=_(u'Description'), blank=True, null = True, default=' ')
    meta_keywords = models.TextField(blank=True, null = True)
    meta_title = models.CharField(max_length=255, blank=True, null = True)
    meta_description = models.TextField(blank=True, null = True)
    is_new = models.BooleanField(verbose_name=_('Is new?'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField()
    
    @property
    def get_image(self):
        clear_name = self.name_slug.split('--')[1]
        path = '%s%s/%s/images/1.png' % (DATA_DIR,self.course.name_slug,clear_name)
        url = '/static/course/%s/%s/images/1.png' % (self.course.name_slug,clear_name)
        if isfile(path):
            # return path
            return mark_safe('<img class="img-fluid" width="200" src="%s" />' % url)
        else:
            return mark_safe('&nbsp;')

    @property
    def get_image_url(self):
        clear_name = self.name_slug.split('--')[1]
        path = '%s%s/%s/images/1.png' % (DATA_DIR,self.course.name_slug,clear_name)
        url = '/static/course/%s/%s/images/1.png' % (self.course.name_slug,clear_name)
        if isfile(path):
            return url
        else:
            return '/static/images/noimage.png'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'slug': self.name_slug })

    # @property
    # def tags(self):    
    #     return Tag.objects.get_for_object(self)

    @property
    def has_video(self):
        cnt = Topic.objects.filter(lesson=self,has_video=True).count()
        if cnt == 0:
            return False
        else:
          return True    

    @property
    def video_icon(self):
        cnt = Topic.objects.filter(lesson=self,has_video=True).count()
        if cnt > 0:
            return mark_safe('<i class="ni ni-button-play text-blue"></i>')
        else:
            return '' 

    def is_paid(self,user):
        from cabinet.models import LogShow
        if ALL_FREE:
            return True
        # if self.number == 1:
        #     return True
        cnt = Topic.objects.filter(lesson=self,has_video=True).count()
        if cnt == 0:
            return True
        # if user.is_superuser:
        #     return True
  
        try:
            LogShow.objects.get(user=user,lesson=self, is_paid=True)
            return True
        except:
            return False

register(Lesson)

class Topic(models.Model):
    title = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    filename = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name=_(u'Lesson'), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=_(u'Course'), on_delete=models.CASCADE)
    video = models.CharField(verbose_name='Video',max_length=250, blank=True)
    has_video = models.BooleanField(default=False)
    is_youtube = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateField()

    def get_clear_lesson_slug(self):
        return self.lesson.name_slug.split('--')[1]



    @property
    def short_content(self):
        path = '%s/%s/%s/%s' % (DATA_DIR,self.lesson.course.name_slug,self.get_clear_lesson_slug(),self.filename)
        if os.path.isfile(path):
            f = open(path,'r')
            txt = f.read()
            txt = self.parse_subject_txt(txt)
            f.close()
            html =  parse_md(txt)
            soup = BeautifulSoup(html, 'html.parser')
            ps = soup.find_all('p')
            cs = soup.find_all('pre')
            imgs = soup.find_all('img')
            out = ''
            for p in ps[0:6]:
                out = out + str(p)
            for c in cs[0:2]:
                out = out + str(c)
            for im in imgs[0:1]:
                out = out + str(im)
            return out
        else:
            return 'File %s does not exist!' % path

    @property
    def content(self):
        path = '%s/%s/%s/%s' % (DATA_DIR,self.lesson.course.name_slug,self.get_clear_lesson_slug(),self.filename)
        #return path
        if os.path.isfile(path):
            f = open(path,'r')
            txt = f.read()
            txt = self.parse_subject_txt(txt)
            return parse_md(txt)
            f.close()
        else:
            return 'File %s does not exist!' % path

    def __str__(self):
        return self.title

    def check_video(self,data):
        vpath = join(VIDEO_DIR,self.course.name_slug)
        # if self.filename == 'py-bs4.md':
        #     import pdb; pdb.set_trace()
        onlyfiles = []
        if isdir(vpath):
            onlyfiles = [f for f in listdir(vpath) if isfile(join(vpath, f))]
        # print(data)
        
        if "youtube" in data:
            self.is_youtube = True
            self.video = data['youtube']
            self.has_video = True
            self.save()
            self.lesson.is_active = True
            self.lesson.save()
            return True
        else:

            for video in onlyfiles:
                fname = video.split('.')[0]
                # print('%s===%s' % (fname,self.filename.split('.')[0]))
                if fname == self.filename.split('.')[0]:
                    self.has_video = True
                    self.video = video
                    self.has_video = True
                    self.save()
                    self.lesson.is_active = True
                    self.lesson.save()
                    return True
        self.video = ''
        self.has_video = False
        self.is_youtube = False
        self.save()
        

    @property
    def video_tag(self):
        if self.is_youtube:
            out = '<iframe width="560" height="315" src="%s" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>' % self.video
            return mark_safe(out)
        if self.has_video:
            return mark_safe('<video controls><source src="/static/video/%s/%s" type="video/mp4"></video>' % (self.course.name_slug,self.video))
        else:
            return ''


    def parse_subject_txt(self,txt):
        pathtosubject = '/media/course/%s/%s' % (self.lesson.course.name_slug, self.get_clear_lesson_slug())
        txt = txt.replace('{path-to-subject}',pathtosubject)
        return txt


# PAYMENT MODEL

from django.contrib.auth.models import User

class LessonPayments(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null = True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null = True)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   
  
################################   

from mptt.models import MPTTModel, TreeForeignKey

class Comments(MPTTModel):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null = True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null = True)
    is_published = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['user']

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'id': self.id })

    @property
    def get_count(self):
        return self.get_children().count()


class Subscription(models.Model):
    email = models.CharField(max_length=250, blank=True, verbose_name=_(u'Email'), unique=True)
    is_subscribed = models.BooleanField(default=False)

class Catalog(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=250, blank=True, verbose_name=_(u'Title'))
    filename = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    catalog = models.ForeignKey(Catalog, on_delete=models.SET_NULL, blank=True, null = True)
    meta_keywords = models.TextField(blank=True, null = True)
    meta_title = models.CharField(max_length=255, blank=True, null = True)
    meta_description = models.TextField(blank=True, null = True)

    def get_absolute_url(self):
        alias = '%s-%s' % (self.catalog,self.filename.split('.')[0])
        return reverse('article_detail', kwargs={'slug': alias })

    @property
    def content(self):
        path = join(DATA_DIR,'articles',self.catalog.name,self.filename)
        if os.path.isfile(path):
            f = open(path,'r')
            txt = f.read()
            txt = self.parse_subject_txt(txt)
            return parse_md(txt)
            f.close()
        else:
            return 'File %s does not exist!' % path

    def parse_subject_txt(self,txt):
        pathtosubject = '/media/course/articles/%s/%s' % \
                        (   self.catalog.name, \
                            self.filename.split('.')[0] \
                        )
        txt = txt.replace('{path-to-subject}',pathtosubject)
        return txt

    def __str__(self):
        return self.title

from sb.settings import DOMAIN

class NewsLetter(models.Model):
    title = models.CharField(max_length=250, blank=True, verbose_name=_(u'Title'))
    lesson = models.ManyToManyField(Lesson, verbose_name=_(u'Content'))
    desc = models.TextField()

    def get_absolute_url(self):
        return reverse('unsubscribe')

    @property
    def txt_content(self):
        out = 'У нас появились новые уроки /n'
        for l in self.lesson.all():
            html = '''
                    Курс:  %s  Урок: %s /n
                    %s%s
            ''' % (l.course.name,l.title, DOMAIN,l.course.get_absolute_url())
            
            out = out +'/n' + html
        unlink = ' /n Чтобы отписаться от рассылки %s%s' % (DOMAIN,self.get_absolute_url())
        return out + ' /n ' + self.desc + unlink + ' /n http://webmonstr.com'

    @property
    def content(self):
        out = '<h1>У нас появились новые уроки</h1>'
        for l in self.lesson.all():
            html = '''
                <p>
                    Курс: <a target=_blank href="%s%s"> %s </a> Урок: <a target=_blank  href="%s%s"> %s </a>
                </p>
            ''' % (DOMAIN,l.course.get_absolute_url(),l.course.name, DOMAIN,l.get_absolute_url(),l.title)
            unlink = '<p><a target=_blank  href="%s%s">Отписаться от рассылки</a></p>' % (DOMAIN,self.get_absolute_url())
            out = out +'<br />' + html
        return mark_safe(out + '<br />' + self.desc + '<br /><br /><br />' + unlink )
