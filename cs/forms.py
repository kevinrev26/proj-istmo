from django import forms
from .models import CustomerSupportTicket


class CustomerSupportTicketForm(forms.ModelForm):
    class Meta:
        model = CustomerSupportTicket
        fields = ['title', 'description', 'image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({"accept" : "image/*"})
        self.fields['image'].required = False  # Making image opt.