from course.models import  Course, Lesson, Topic
from pl.settings import DATA_DIR, VIDEO_DIR
from os import listdir
from os.path import isfile, join, isdir

import yaml
from django.core.files import File

from .models import Catalog, Article

class ArticleLoader(object):

    def __init__(self, *args, **kwargs):
        self.dir = args[0]

    def process(self):
        print('process .. %s' % self.dir)
        self.create_catalogs()
        self.save_articles()

    def create_catalogs(self):
        try:
            self.catalog = Catalog.objects.get(name=self.dir)
        except:
            self.catalog = Catalog.objects.create(name=self.dir)

    def save_articles(self):
        path = join(DATA_DIR,'articles',self.dir,'meta.yml')
        print('Saving articles from %s' % path)
        meta = self.get_meta(path)
        if 'files' in meta:
            for file in meta['files']:
                try:
                    article = Article.objects.get(filename=file['file'])
                except:
                    article = Article()
                article.filename = file['file']
                article.title = file['title']
                article.catalog = self.catalog
                article.meta_description = file['meta_description']
                article.meta_keywords = file['meta_keywords']
                article.meta_title = file['meta_title']
                article.save()
                print('Saving ... %s' % article.filename)
            
    def get_meta(self,path):
        if isfile(path):
            f = open(path,'r')
            str = f.read()
            f.close()
            yml = yaml.load(str, Loader=yaml.FullLoader)
            return yml
        else:
            return {}

    @staticmethod
    def get_active_catalog_dirs():
        out = []
        onlydirs = [f for f in listdir(DATA_DIR+'/articles') if isdir(join(DATA_DIR+'/articles', f))]
        for d in onlydirs:
            if d.find('.') == -1:
                out.append(d)
        return out


