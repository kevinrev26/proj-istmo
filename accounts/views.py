from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from .utils import send_activation_email

def signup(request):
    template_data = {}
    template_data['title'] = 'Sing Up'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form  = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            user = form.save(commit=False)
            # Send activation email
            user.is_active = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_url = request.build_absolute_uri(
                reverse('accounts.activate', kwargs={'uidb64': uid, 'token': token})
            )
            
            send_activation_email(user, activation_url)
            
            messages.info(request, "Por favor revisa tu correo para activar tu cuenta.")
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data' : template_data})
        
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})

    elif request.method == 'POST':
        user  = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = "Invalid credentials"
            return render(request, 'accounts/login.html', {'template_data': template_data})
        elif not user.is_active:
            messages.warning(request, "Tu cuenta no está activada. Por favor revisa tu correo electrónico para el enlace de activación.")
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "¡Tu cuenta ha sido activada! Ahora puedes iniciar sesión.")
        return redirect('accounts.login')
    else:
        messages.error(request, "El enlace de activación es inválido o ha expirado.")
        return redirect('home.index')
