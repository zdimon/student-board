from django.shortcuts import render
from course.models import parse_md
from sb.settings import DATA_DIR

def index(request):
    path = DATA_DIR+f'/index_{request.LANGUAGE_CODE}.md'
    f = open(path, 'r')
    txt = f.read()
    f.close()
    index = parse_md(txt)    
    return render(request, 'dash/index.html', {'text': index})
