from django.shortcuts import render
from sb.settings import DATA_DIR
from course.models import parse_md

def delivery(request):
    path = DATA_DIR+'/delivery.md'
    f = open(path, 'r')
    txt = f.read()
    f.close()
    oferta = parse_md(txt)    
    return render(request,'md.html', {'text': oferta})   
