from django.shortcuts import render
from course.models import parse_md
from sb.settings import DATA_DIR, TEST_MODE
from course.models import Course, Kursak
from django.utils import translation

def index(request):
    if TEST_MODE:
        courses = Course.objects.filter(lang=translation.get_language())
    else:
        courses = Course.objects.filter(is_active=True, lang=translation.get_language())
    # kursaks = Kursak.objects.all()
    path = DATA_DIR+f'/about-{translation.get_language()}.md'
    f = open(path, 'r')
    txt = f.read()
    f.close()
    about = parse_md(txt)    
    return render(request, 'dash/index.html', {"courses": courses, "about": about})
