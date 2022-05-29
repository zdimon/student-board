from django.shortcuts import render
from course.models import Course
from django.contrib import messages
from student.models import Student2Course
from sb.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY
from liqpay.liqpay3 import LiqPay


def replanish(request):
    form = None
    if request.method == 'POST':
        amount = request.POST.get('amount')
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        form = liqpay.cnb_form({
            'action': 'pay',
            'amount': amount,
            'currency': 'UAH',
            'description': 'Payment for the lesson',
            'order_id': '%s-%s' % (123,123),
            'version': '3',
            'result_url': 'sssss'
        })        
    return render(request,'student/replanish.html', {"form": form})
