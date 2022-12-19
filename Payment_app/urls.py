from django.urls import path
from Payment_app import views

app_name = 'Payment_App'

urlpatterns = [
    path('checkout/', views.Checkout, name='checkout'),
    path('payment/', views.Payment, name='payment'),
    path('status/', views.Complate, name='status'),
    path('purchase/<val_id>/<tran_id>/', views.Purchase, name='purchase'),
    path('order/view/', views.Order_view, name='order_view')
]
