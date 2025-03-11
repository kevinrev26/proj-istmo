from django.urls import path
from . import views
urlpatterns = [
    path('', views.show, name='shop.show'),
    path('analytics', views.show_analytics, name='shop.analytics'),
]