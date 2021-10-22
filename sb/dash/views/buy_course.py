from django.shortcuts import render
from course.models import Course
from student.models import Student2Course, StudentPayment
from liqpay.liqpay3 import LiqPay
from sb.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY, DOMAIN
from django.urls import reverse


def buy_course(request,course_id):
    course = Course.objects.get(pk=course_id)
    p = StudentPayment()
    p.user = request.user.student
    p.course = course
    p.save()
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    form_html = liqpay.cnb_form({
        'action': 'pay',
        'amount': 1500,
        'currency': 'UAH',
        'description': 'Payment for the course',
        'order_id': '%s' % p.id,
        'version': '3',
        'result_url': DOMAIN+reverse('pay-success'),
        'server_url':  DOMAIN+reverse('pay-process')
    })
    
    return render(request, 'dash/buy_course.html', {"course": course, "form_html": form_html})
