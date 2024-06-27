from django.utils import translation
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from sb.local import DOMAIN
from django.utils.translation import get_language

def set_lang(request,lang):
    translation.activate(lang)
    next = request.GET.get('next', None)

    # if not next:
    #     next = '/'
    # else:
    #     tmp = next.split('/')[2:]
    #     tmp.insert(0,lang)
    #     next = '/'.join(tmp)
    #     next = next.replace('-'+get_language(),lang)
        
    next = '/'+lang
    return HttpResponseRedirect('%s%s' %  (DOMAIN,next))