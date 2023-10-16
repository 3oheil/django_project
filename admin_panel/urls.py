from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_admin'),
    path('product-admin/', views.ProductList.as_view(), name='product_admin'),
    path('product-admin/edit/<pk>', views.EditProductAdminView.as_view(), name='product_edit_admin'),
    path('contact-admin/', views.ContactUsView.as_view(), name='contact_admin'),
    path('contact-admin/edit/<pk>', views.EditContactFormView.as_view(), name='contact_edit_admin'),
    path('articles-admin/', views.ArticleListView.as_view(), name='article_admin'),
    path('articles/edit/<pk>', views.ArticleEditView.as_view(), name='admin_edit_article'),
]
