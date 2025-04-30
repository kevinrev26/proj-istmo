from django.urls import path
from . import views
urlpatterns = [
    path('', views.show, name='shop.show'),
    path('analytics', views.show_analytics, name='shop.analytics'),
    path('inventory', views.show_inventory, name='shop.inventory'),
    path('orders', views.show_orders, name='shop.orders'),
    path('chat', views.show_chat, name='shop.chat'),
    path('add_product', views.add_product, name='shop.add_product'),
    path('add_stock/<int:product_id>/', views.add_stock, name='shop.add_stock'),
]