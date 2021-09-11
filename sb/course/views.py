from django.shortcuts import render
from django.http import HttpResponse
from course.models import Course, Lesson, Comments, Subscription
from cabinet.models import ReplCredit, UserProfile
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from pl.settings import LESSON_PRICE
from django.contrib.auth.decorators import login_required

from liqpay.liqpay3 import LiqPay
from pl.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY, LIQPAY_PROCESS_URL, DOMAIN, LESSON_PRICE
import time
from .models import LessonPayments, Topic
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from pl.settings import DATA_DIR
from course.models import parse_md
from cabinet.models import LogShow
from tagging.models import Tag, TaggedItem

@login_required
def pay(request,lesson_id):
    if request.user.userprofile.account<2:
        messages.info(request, 'У вас кредитов то нету :-(')
        return redirect(reverse('add_credits'))
    else:
        lesson = Lesson.objects.get(pk=lesson_id)
        user = request.user.userprofile
        user.account = user.account - 2
        user.save()
        ls = LogShow.objects.get(user=request.user.userprofile,lesson=lesson)
        ls.is_paid = True
        ls.save()
        
        return redirect(reverse('show_lesson', kwargs={'id': lesson.id}))

    
   

from django.views.decorators.csrf import csrf_exempt

from course.utils import get_credits

@csrf_exempt
def liqpay_process(request):
    print(request.POST)
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    data = request.POST.get('data')
    signature = request.POST.get('signature')
    sign = liqpay.str_to_sign(LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY)
    if sign == signature:
        print('callback is valid')
        data = liqpay.decode_data_from_str(data)
        idr = data['order_id'].split('-')[1]
        idu = data['order_id'].split('-')[0]
        order = ReplCredit.objects.get(pk=idr)
        order.is_paid = True
        order.save()
        user = UserProfile.objects.get(pk=idu)
        user.account = user.account + get_credits(order.ammount)
        user.save()
    return HttpResponse('ok')

def course_detail(request,slug):
    course = Course.objects.get(name_slug=slug)
    lessons = Lesson.objects.filter(course=course).order_by('number')
    paid = []
    for l in lessons:
        if l.is_paid(request.user):
            paid.append(l.id)
    print(paid)
    return render(request,'course_detail.html',{'course': course, 'lessons': lessons, 'paid': paid, 'price': LESSON_PRICE})


@csrf_exempt
def lesson_detail(request,slug):
    lesson = Lesson.objects.get(name_slug=slug)
    topics = Topic.objects.filter(lesson=lesson).order_by('order')
    is_free = lesson.is_paid(request.user)
    try:
        try:
            LogShow.objects.get(lesson=lesson,user=request.user.userprofile)
        except:
            ls = LogShow()
            ls.lesson = lesson
            ls.user = request.user.userprofile
            ls.save()
    except Exception as e:
        print(str(e))
    return render(request,'lesson_detail.html',{'lesson': lesson, 'is_free': is_free, 'topics': topics})


@login_required
def my_cabinet(request):
    payments = LessonPayments.objects.filter(user=request.user).order_by('-id')
    return render(request,'my_cabinet.html',{'payments': payments})

@login_required
def save_comment(request):
    if request.method == 'POST':
        lesson = Lesson.objects.get(pk=request.POST.get('lesson_id'))
        comment = Comments()
        comment.lesson = lesson
        comment.user = request.user
        comment.content = request.POST.get('message')
        comment.is_published = True
        comment.save()
        messages.info(request, 'Спасибо. Ваш комментарий был сохранен.')
        return redirect(lesson)

@login_required
def discussion(request):
    comments = Comments.objects.filter(is_published=True, level=0).order_by('-id')
    return render(request,'discussion.html',{'comments': comments})

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            s = Subscription()
            s.email = email
            s.is_subscribed = True
            s.save()
            messages.info(request, 'Спасибо, вы успешно подписаны.')
        except:
            messages.info(request, 'Вы уже подписаны.')
    return redirect('/')

from course.models import Catalog

def articles(request):
    catalog = Catalog.objects.all()
    return render(request,'articles.html',{'catalog': catalog})

from course.models import Article, Catalog

def article_detail(request,slug):
    tmparr =  slug.split('-')
    filename = ('-').join(tmparr[1:len(tmparr)])+'.md'
    catalogsename = slug.split('-')[0]
    catalog = Catalog.objects.get(name=catalogsename)
    article = Article.objects.get(filename=filename)
    return render(request,'article_detail.html',{'article': article})

def pay_success(request,lesson_id):
    lesson = Lesson.objects.get(pk=request.POST.get('lesson_id'))
    messages.info(request, 'Спасибо. <a href="%s">Просмотр урока</a>' % lesson.get_absolute_url)


def comment_detail(request,id):
    comment = Comments.objects.get(pk=id)
    return render(request,'comment_detail.html',{'comment': comment})


def sitemap(request):
    courses = Course.objects.all().order_by('-id')
    return render(request,'map.html',{'courses': courses})


def unsubscribe(request):
   
    try:
        s = Subscription.objects.get(email=request.user.username)
        s.is_subscribed = False
        s.save()
        messages.info(request, 'Вы отписались от рассылки.')
    except:
        messages.info(request, 'Емейл %s не подписаны на рассылку.' % request.user.username)

    return redirect('/')

def show_tag(request,tag):
    tag = Tag.objects.get(name=tag)
    lessons = TaggedItem.objects.get_by_model(Lesson, tag)
    tags = Tag.objects.all().order_by('name')
    return render(request,'tag_show.html',{ \
        'tag': tag, \
        'lessons': lessons, \
        'tags': tags
        })