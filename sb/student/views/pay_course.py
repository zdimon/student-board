from django.shortcuts import render
from mentor.models import Invitation
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from student.models import Student, CoursePayment
import random
from student.tasks import pay_course_notification
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import ugettext as _
from course.models import Course
import random
from django.contrib.auth import login
from sb.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY, DOMAIN, TEST_MODE
from liqpay.liqpay3 import LiqPay

def pay_course(request, course_id):
    course = Course.objects.get(name_slug=course_id)
    if request.user.is_authenticated:
        try:
            lp = CoursePayment.objects.get(user=request.user.student, course=course)
        except:
            lp = CoursePayment()
            lp.user = request.user.student
            lp.course = course
            lp.save()
        return redirect('pay-course-button', payment_id=lp.pk)        
    if request.method == 'POST':
        paswd = random.randint(1111,9999)
        email = request.POST.get('username')
        name = request.POST.get('name')
        try:
            student = Student.objects.get(email=email)
        except: 
            student = Student()
            student.username = email
            student.email = email
            student.is_active = True
            student.set_password(paswd)
            student.save()
            messages.info(request, _('Вы были зарегистрированы, авторизованы, и вам выслан емейл с паролем на сайт. Можно оплачивать курс.'))
        lp = CoursePayment()
        lp.user = student
        lp.course = course
        lp.save()
        login(request, student)
        return redirect('pay-course-button', payment_id=lp.pk)
    return render(request,'student/pay_course.html', {'course': course})

def pay_course_button(request, payment_id):
    payment = CoursePayment.objects.get(pk=payment_id)
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    print(payment.course.cost)
    form = liqpay.cnb_form({
        'action': 'pay',
        'amount': payment.course.cost,
        'currency': 'UAH',
        'description': 'Payment for the course',
        'order_id': '%s-%s' % (payment.pk, payment.user.student.pk),
        'version': '3',
        'result_url': DOMAIN+reverse('pay-success'),
        'server_url':  DOMAIN+reverse('pay-course-process')
    }) 
    return render(request,'student/pay_course_button.html', {'payment': payment, "form": form, 'test_mode': TEST_MODE})

def pay_course_test(request,course_id):
    course = Course.objects.get(pk=course_id)
    order = CoursePayment.objects.get(user=request.user.student, course=course)
    order.is_approved = True
    order.save()
    messages.info(request, _('Вы оплатили курс.'))    
    return redirect(reverse('detail-course-student', kwargs ={"course_id":course.pk}))

def pay_course_from_account(request,course_id):
    course = Course.objects.get(pk=course_id)
    student = request.user.student
    if student.account > course.cost:
        student.account = student.account - course.cost
        student.save()
    else:
        messages.info(request, _('У вас недостаточно средств на счету.'))
        return redirect(reverse('detail-course-student', kwargs ={"course_id":course.pk}))        
    try:
        order = CoursePayment.objects.get(user=request.user.student, course=course)
    except:
        order = CoursePayment.objects.create(user=request.user.student, course=course)
    order.is_approved = True
    order.save()
    pay_course_notification(course,student)
    messages.info(request, _('Вы оплатили курс.'))    
    return redirect(reverse('detail-course-student', kwargs ={"course_id":course.pk}))