from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductList.as_view(), name='product_category_list'),
    path('brand/<brand>', views.ProductList.as_view(), name='product_brand_list'),
    path('product-favorite', views.AddProductFavorite.as_view(), name='add_product_favorite'),
    path('<slug:slug>', views.ProductDetail.as_view(), name='product_detail'),

]
