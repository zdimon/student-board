from django.shortcuts import render
from course.models import parse_md
from sb.settings import DATA_DIR
from course.models import Course

def index(request):
    courses = Course.objects.all()
    path = DATA_DIR+f'/index_ru.md'
    f = open(path, 'r')
    txt = f.read()
    f.close()
    index = parse_md(txt)    
    return render(request, 'dash/index.html', {'text': index, "courses": courses})
