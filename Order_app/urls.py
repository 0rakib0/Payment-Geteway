from django.urls import path
from Order_app import views
app_name = 'Order_App'


urlpatterns = [
    path('add_item/<id>/', views.Add_to_cart, name='add'),
    path('cart/', views.Cart_view, name='carts'),
    path('remove/item/from/card/<pk>/', views.remove_from_cart, name='remove_item'),
    path('increase/<pk>/', views.increase, name='increase'),
    path('dicress/<pk>/', views.dicress, name='dicress'),
]
