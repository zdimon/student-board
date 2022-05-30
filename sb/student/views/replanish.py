from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course, Replanishment
from sb.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY
from liqpay.liqpay3 import LiqPay
from sb.settings import DOMAIN
from django.urls import reverse


def replanish(request):
    form = None
    if request.method == 'POST':
        amount = request.POST.get('amount')
        r = Replanishment()
        r.ammount = amount
        r.user = request.user.student
        r.save()
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        form = liqpay.cnb_form({
            'action': 'pay',
            'amount': amount,
            'currency': 'UAH',
            'description': 'Payment for the lesson',
            'order_id': '%s-%s' % (r.pk, request.user.student.pk),
            'version': '3',
            'result_url': DOMAIN+reverse('pay-success'),
            'server_url':  DOMAIN+reverse('pay-process')
        })        
    return render(request,'student/replanish.html', {"form": form})
