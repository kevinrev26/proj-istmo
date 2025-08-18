from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Review, Wishlist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.
def show_item(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product=product)
    template_data = {}
    template_data['product'] = product
    template_data['reviews'] = reviews
    return render(request, 'ecommerce/show.html', {'template_data' : template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        product = Product.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.product = product
        review.user = request.user
        review.save()
        return redirect('ecommerce.show', id=id)
    else:
        return redirect('ecommerce.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('ecommerce.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'ecommerce/edit_review.html', {'template_data' : template_data})
    if request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('ecommerce.show', id=id)
    else:
        return redirect('ecommerce.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('ecommerce.show', id=id)

@require_POST
@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        liked = False
    else:
        wishlist.products.add(product)
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'wishlist_count': wishlist.products.count()
    })

@login_required
def wishlist_view(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist_products = wishlist.products.all()
    
    return render(request, 'ecommerce/wishlist.html', {
        'wishlist_products': wishlist_products
    })