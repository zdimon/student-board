from django.core.management.base import BaseCommand, CommandError
from course.article_loader import ArticleLoader
from pl.settings import DATA_DIR

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('Start loading courses from %s' % DATA_DIR)
        for d in ArticleLoader.get_active_catalog_dirs():
            loader = ArticleLoader(d)
            loader.process()