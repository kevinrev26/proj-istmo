from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.show_item, name='ecommerce.show')
]