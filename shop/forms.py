from django import forms
from .models import Shop
from ecommerce.models import Product

from django import forms
from .models import Shop
from ecommerce.models import Category

class ShopForm(forms.ModelForm):
    # Explicitly define fields that need custom attributes/widgets
    terms_accepted = forms.BooleanField(
        required=True,
        label="Acepto los Términos para Comerciantes",
        help_text="Confirmo que tengo derecho a vender estos productos"
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True),  # Only show main categories
        label="Categoría Principal*",
        empty_label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Shop
        fields = [
            'name', 
            'description', 
            'logo', 
            'category',
            'contact_email',
            'phone',
            'address',
            'terms_accepted'
        ]
        labels = {
            'name': 'Nombre de la Tienda*',
            'description': 'Descripción*',
            'logo': 'Logo de la Tienda',
        }
        help_texts = {
            'name': 'Este será el nombre público de tu tienda (mínimo 4 caracteres)',
            'description': 'Describe los productos que ofrecerás (mínimo 20 caracteres)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'logo': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap or custom classes to all fields
        for field in self.fields:
            if field != 'terms_accepted':  # Don't add to checkbox
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 4:
            raise forms.ValidationError("El nombre debe tener al menos 4 caracteres.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 20:
            raise forms.ValidationError("La descripción debe tener al menos 20 caracteres.")
        return description
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'subcategory']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({"accept" : "image/*"})