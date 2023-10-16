from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView
from django.views.generic.list import ListView

from article_module.models import Article
from contact_module.forms import ContactUsForm
from contact_module.models import ContactUs
from product_module.models import Product
from utils.my_decorators import permission_checker_decorator


# Create your views here...


@permission_checker_decorator
def index(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'admin_panel/home/index.html')
    return redirect(reverse('login_page'))


@method_decorator(permission_checker_decorator, name='dispatch')
class ArticleListView(ListView):
    model = Article
    template_name = 'admin_panel/admin_articles/articles_page.html'
    paginate_by = 2
    context_object_name = 'admin_articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        query = super().get_queryset()
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


@method_decorator(permission_checker_decorator, name='dispatch')
class ArticleEditView(UpdateView):
    model = Article
    template_name = "admin_panel/admin_articles/edit_articles_page.html"
    fields = '__all__'
    success_url = '/panel-admin/articles-admin/'


class ProductList(ListView):
    model = Product
    template_name = 'admin_panel/product/admin_product_page.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        return context

    def get_queryset(self):
        query = super().get_queryset()
        return query


class EditProductAdminView(UpdateView):
    template_name = 'admin_panel/product/edit_product_admin_page.html'
    model = Product
    fields = "__all__"
    success_url = '/panel-admin/product-admin/'


class ContactUsView(CreateView):
    template_name = 'admin_panel/contact_admin/contact_admin_page.html'
    model = ContactUs
    form_class = ContactUsForm
    success_url = '/panel-admin/contact-admin/'
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditContactFormView(UpdateView):
    template_name = 'admin_panel/contact_admin/contact_admin_page.html'
    model = ContactUs
    fields = '__all__'
    success_url = '/panel-admin/contact-admin/'
