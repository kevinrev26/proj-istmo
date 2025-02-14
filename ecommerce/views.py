from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Review
from django.contrib.auth.decorators import login_required

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
