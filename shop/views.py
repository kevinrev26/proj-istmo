from django.shortcuts import render, redirect
from .models import Shop
from django.contrib.auth.decorators import login_required
from .forms import ShopForm

@login_required
def show(request):
    user_shop = Shop.objects.filter(owner=request.user).first()
    print(user_shop)
    if not user_shop:
        if request.method == "POST":
            form = ShopForm(request.POST, request.FILES)
            if form.is_valid():
                # So if you commit=False, the form is save in "memory" onlt
                shop = form.save(commit=False)
                shop.owner = request.user
                shop.save()

                print("Shop created:", shop)  # Debugging print
                print("All shops:", Shop.objects.all())  # Check if it's really saved
                return redirect('shop.show')
            else:
                template_data = {}
                template_data['form'] = form
                print("Form errors:", form.errors)
                return render(request, 'shop/shop_creation.html', {'template_data': template_data})
        else:
            form = ShopForm()
            template_data = {}
            template_data['form'] = form
            return render(request, 'shop/shop_creation.html', {'template_data': template_data})
    else:
        return render(request, 'shop/show.html', {'shop': user_shop})