from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.show_item, name='ecommerce.show'),
    path('<int:id>/review/create/', views.create_review, name='ecommerce.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='ecommerce.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='ecommerce.delete_review'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]