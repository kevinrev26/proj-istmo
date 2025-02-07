from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
]