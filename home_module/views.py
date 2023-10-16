from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from product_module.models import Product, ProductCategory
from site_setting.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list


class HomePageView(TemplateView):
    template_name = 'shared/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True)
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visit_products = Product.objects.filter(is_delete=False, is_active=True).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = group_list(latest_products)
        context['most_visit_products'] = group_list(most_visit_products)
        categories = list(
            ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(is_active=True,
                                                                                                is_delete=False,
                                                                                                products_count__gt=0)[
            :6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)
        context['categories_products'] = categories_products

        most_bought_products = Product.objects.filter(orderdetail__order__is_pain=True).annotate(
            order_count=Sum('orderdetail__count')).order_by('-order_count')[:12]

        context['most_bought_products'] = group_list(most_bought_products)

        return context


def site_header_partial(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_mean_site=True).first()
    context = {
        'site_setting': site_setting
    }
    return render(request, 'shared/site_header_partial.html', context)


def header_component_partial(request):
    return render(request, 'shared/header_component_references.html', {})


def footer_references_partial(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_mean_site=True).first()
    footer_link_boxs = FooterLinkBox.objects.all()
    for item in footer_link_boxs:
        item.footerlink_set
    context = {
        'site_setting': site_setting,
        'footer_link_boxs': footer_link_boxs
    }
    return render(request, 'shared/site_footer_partial.html', context)


def footer_component_partial(request):
    return render(request, 'shared/footer_component_partial.html')


class AboutUsView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        site_setting = SiteSetting.objects.filter(is_mean_site=True).first()
        context['site_setting'] = site_setting
        return context
