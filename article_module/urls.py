from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_page'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail_page'),
    path('add-article-commend', views.add_article_comment, name='add_article_comment_page'),
]
