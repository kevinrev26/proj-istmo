from django.urls import path
from . import views
urlpatterns = [
    path('', views.show, name='shop.show'),
    path('inventory', views.show_inventory, name='shop.inventory'),
    path('orders', views.show_orders, name='shop.orders'),
    path('orders/<int:order_id>/', views.show_order_details, name='shop.order_detail'),
    path('orders/<int:order_id>/update_status/', views.update_order_status, name='shop.update_order_status'),
    path('chat', views.show_chat, name='shop.chat'),
    path('add_product', views.add_product, name='shop.add_product'),
    path('add_stock/<int:product_id>/', views.add_stock, name='shop.add_stock'),
]