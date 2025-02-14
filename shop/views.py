from django.shortcuts import render
from .models import Shop
from django.contrib.auth.decorators import login_required

@login_required
def show(request, id):
    template_data = {}


    return render(request, 'shop/show.html', {'template_data': template_data})