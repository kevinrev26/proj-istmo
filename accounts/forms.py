from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
import phonenumbers
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django_countries import countries

class CustomErrorList(ErrorList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Ensures compatibility with Django

    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert"> {e}</div>'
            for e in self
        ]))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )
    country_code = forms.ChoiceField(
        choices=[('', 'Seleccionar país')] + [
            (f"+{phonenumbers.country_code_for_region(code)}", f"{name}")
            for code, name in countries
            if phonenumbers.country_code_for_region(code)
        ],
        widget=forms.Select(attrs={
            'class': 'form-select country-select-flag',
            'data-live-search': 'true'
        }),
        required=True,
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Número",
        help_text="Sin código de país"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'country_code', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        phone_number = cleaned_data.get('phone_number')
        
        if country_code and phone_number:
            full_number = f"{country_code}{phone_number}"
            try:
                parsed = phonenumbers.parse(full_number, None)
                if not phonenumbers.is_valid_number(parsed):
                    self.add_error('phone_number', "Número de teléfono inválido")
                cleaned_data['phone_number'] = phonenumbers.format_number(
                    parsed, 
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
            except phonenumbers.phonenumberutil.NumberParseException:
                self.add_error('phone_number', "Formato de teléfono incorrecto")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.profile.phone_number = self.cleaned_data["phone_number"]
            user.profile.save()
        return user
