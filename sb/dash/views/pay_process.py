from django.shortcuts import render
from liqpay.liqpay3 import LiqPay
from sb.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pay_process(request):
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    data = request.POST.get('data')
    signature = request.POST.get('signature')
    sign = liqpay.str_to_sign(LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY)
    if sign == signature:
        print('callback is valid')
    response = liqpay.decode_data_from_str(data)
    print('callback data', response)
    return render(request, 'dash/pay_success.html')
