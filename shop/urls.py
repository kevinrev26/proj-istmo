from django.urls import path
from . import views
urlpatterns = [
    path('', views.show, name='shop.show'),
    path('analytics', views.show_analytics, name='shop.analytics'),
    path('inventory', views.show_inventory, name='shop.inventory'),
    path('chat', views.show_chat, name='shop.chat'),
]