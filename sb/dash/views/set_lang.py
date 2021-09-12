from django.utils import translation
from django.shortcuts import redirect


def set_lang(request,lang):
    translation.activate(lang)
    return redirect('/')