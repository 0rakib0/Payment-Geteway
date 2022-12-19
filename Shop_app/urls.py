from django.urls import path
from Shop_app import views
app_name = 'Shop_App'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/details/<pk>/', views.ProdustDetails.as_view(), name='product_view')
]
