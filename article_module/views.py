from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from site_setting.models import SiteBanner
from .models import Article, ArticleCategory, ArticleCommends


# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'article_module/article_page.html'
    paginate_by = 2
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.PositionBannerChoices.product_list)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article: Article = kwargs.get('object')
        context['commends'] = ArticleCommends.objects.filter(article_id=article.id, parent=None).order_by(
            '-create_deta').prefetch_related(
            'articlecommends_set')
        return context


def article_category_partial(request: HttpRequest):
    article_main_category = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                                   parent_id=None)
    context = {
        'main_categories': article_main_category
    }
    return render(request, 'article_module/component/article_category.html', context)


def add_article_comment(request: HttpRequest):
    article_id = request.GET.get('article_id')
    article_comment = request.GET.get('article_comment')
    parent_id = request.GET.get('parent_id')
    new_article_comment = ArticleCommends(article_id=article_id, text=article_comment, user_id=request.user.id,
                                          parent_id=parent_id)
    new_article_comment.save()
    return HttpResponse('Response')
