from django.urls import path
from . import views

urlpatterns = [
    path('add-to-order', views.add_to_order, name='add_to_order'),
    path('request-pyment/', views.request_pyment, name='request'),
    path('verify-pyment/', views.verify_pyment, name='verify'),
]
