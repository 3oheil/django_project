from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView
from django.views.generic.list import ListView

from site_setting.models import SiteBanner
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from utils.http_servis import get_client_ip
from utils.convertors import group_list


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'product_module/product_list_page.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 1000000
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.PositionBannerChoices.product_list)
        return context

    def get_queryset(self):
        query = super(ProductList, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__exact=category_name)
        return query


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_module/product_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get('product-favorite')
        context['is_favorite'] = favorite_product_id == str(loaded_product)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.PositionBannerChoices.product_detail)

        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries'] = group_list(galleries, 3)
        context['related_products'] = group_list(
            list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()
        return context


class AddProductFavorite(View):
    def post(self, request: HttpRequest):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)
        request.session['product-favorite'] = product_id
        return redirect(product.get_absolute_url())


def product_category_component(request: HttpRequest):
    product_category = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_category
    }
    return render(request, 'product_module/component/product_category_component.html', context)


def product_brand_component(request: HttpRequest):
    product_brand = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brand
    }
    return render(request, 'product_module/component/product_brand_page.html', context)
