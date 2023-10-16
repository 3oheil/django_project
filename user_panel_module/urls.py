from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelView.as_view(), name='user_panel_page'),
    path('edit-profile', views.EditProfileView.as_view(), name='edit_profile_page'),
    path('change-password', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('my-shopping/', views.ShoppingListView.as_view(), name='user_shopping_page'),
    path('my-detail-shopping/<order_id>', views.order_shopping_detail, name='user_detail_shopping_page'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_page'),
    path('change-order-detail', views.change_order_detail, name='change_order_detail_page'),
]
