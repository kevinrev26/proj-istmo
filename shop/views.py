from django.shortcuts import render
from .models import Shop
from django.contrib.auth.decorators import login_required

@login_required
def show(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    template_data = {}

    if not user_shop:
        return render(request, 'shop/shop_creation.html', {'template_data': template_data})
    
    #TODO check for shop creation form.
    
    return render(request, 'shop/show.html', {'shop': user_shop})