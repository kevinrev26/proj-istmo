from django import forms
from .models import Shop
from ecommerce.models import Product

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["name", "description", "logo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].widget.attrs.update({"accept" : "image/*"})
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'subcategory']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({"accept" : "image/*"})