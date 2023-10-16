from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView

from account_module.models import User
from order_module.models import Order, OrderDetail
from .forms import EditForm, ChangePasswordForm

# Create your views here.

method_decorator(login_required, name='dispatch')


class UserPanelView(TemplateView):
    template_name = 'user_panel_module/user_panel_page.html'


method_decorator(login_required, name='dispatch')


class EditProfileView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, "user_panel_module/edit_profile_page.html", context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, "user_panel_module/edit_profile_page.html", context)


method_decorator(login_required, name='dispatch')


class ShoppingListView(ListView):
    model = Order
    template_name = "user_panel_module/shopping_list_page.html"
    context_object_name = 'information'

    def get_queryset(self):
        queryset = super().get_queryset()
        request: HttpRequest = self.request
        queryset = queryset.filter(user_id=request.user.id, is_pain=True)
        return queryset


method_decorator(login_required, name='dispatch')


class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm()
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه است')
        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


login_required


def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_component.html')


login_required


def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_pain=False,
                                                                                             user_id=request.user.id)
    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount
    }

    return render(request, 'user_panel_module/user_basket.html', context)


login_required


def remove_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_pain=False,
                                                             order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'not_found_detail'
        })
    # detail.delete()

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_pain=False,
                                                                                             user_id=request.user.id)

    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount
    }

    render_to_string('user_panel_module/user_basket_component.html', context)
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_component.html', context)
    })


login_required


def change_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__is_pain=False,
                                              order__user_id=request.user.id).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()

    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_pain=False,
                                                                                             user_id=request.user.id)

    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount
    }

    render_to_string('user_panel_module/user_basket_component.html', context)
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_component.html', context)
    })


login_required
def order_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()

    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, "user_panel_module/shopping_detail_page.html", context={'order': order})
