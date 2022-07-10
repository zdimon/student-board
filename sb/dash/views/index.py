from django.shortcuts import render
from course.models import parse_md
from sb.settings import DATA_DIR
from course.models import Course, Kursak
from django.utils import translation

def index(request):
    courses = Course.objects.filter(is_active=True)
    # kursaks = Kursak.objects.all()
    path = DATA_DIR+f'/about-{translation.get_language()}.md'
    f = open(path, 'r')
    txt = f.read()
    f.close()
    about = parse_md(txt)    
    return render(request, 'dash/index.html', {"courses": courses, "about": about})
