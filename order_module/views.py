from datetime import time

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from order_module.models import Order, OrderDetail
from product_module.models import Product

from django.conf import settings
import requests
import json

sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "نهایی سازی خرید محصول شما"  # Required
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/order/verify-pyment/'


def add_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))

    if count < 1:
        return JsonResponse({
            'status': 'count not valid',
            'text': 'محصول با موفقیت به سبد خرید افزوده شد',
            'confirmButtonText': 'مچکرم'
        })

    product = Product.objects.filter(id=product_id, is_delete=False, is_active=True).first()

    if request.user.is_authenticated:
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_pain=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'text': 'محصول با موفقیت به سبد خرید افزوده شد',
                    'confirmButtonText': 'مچکرم',
                    'icon': 'success'
                })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirmButtonText': 'بسیار خب',
                'icon': 'error'
            })

    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای خرید محصول ابتدا می بایست لاگین کنید',
            'confirmButtonText': 'ورود به سایت',
            'icon': 'warning'
        })


@login_required
def request_pyment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_pain=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
def verify_pyment(request: HttpRequest, authority):
    current_order, created = Order.objects.get_or_create(is_pain=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            current_order.is_pain = True
            current_order.pyment_date = time.strftime(self=time)
            current_order.save()
            return {'status': True, 'RefID': response['RefID']}

        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
