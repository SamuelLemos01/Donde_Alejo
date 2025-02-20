from urllib import request
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

from dondealejo import views



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')  # Corregido

        # Verificación de contraseñas
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        # Verificación de existencia de email
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
        # Verificación de existencia de nombre de usuario
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            # Creación del usuario
            user = User.objects.create_user(username=username, email=email, password=password)
            # Intentar autenticar al usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "¡Registro exitoso! Has iniciado sesión.")
                return redirect('login')  # Redirige a una página después de éxito (por ejemplo, home)
            else:
                messages.error(request, "Hubo un problema al iniciar sesión después del registro.")
    
    return render(request, 'register.html')




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Por favor, ingreseambos campos.')
            return render(request, 'login.html')
        
        try: 
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe')
            return render(request, 'login.html')
        
        if user is not None:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                return redirect('bienvenidos')
            else: 
                messages.error(request, "Contraseña incorrecta.")
    return render(request, 'login.html')

from django.shortcuts import render
from .models import Product

def menu(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})







def home (request):
    return render(request, 'home.html')

def bienvenidos (request):
    return render(request, 'bienvenidos.html')

def almuerzo (request):
    return render(request, 'almuerzo.html')
    

def cafeteria (request):
    return render(request, 'cafeteria.html')

def quienes_somos (request):
    return render(request, 'quienes_somos.html')

def carrito (request):
    return render(request, 'carrito.html')

def sesion (request):
    return render(request, 'sesion.html')

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def email (request):
    return render(request, 'email.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name'],
        email = request.POST['email'],
        subject = request.POST['subject'],
        message = request.POST['message'],

        template = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'message': message
        })

        email = EmailMessage (
            subject,
            template,
            settings.EMAIL_HOS_USER,
            ['carenrojas212005@gmail.com']
        )

        email.fail.silently = False
        email.send()

        messages.success(request, 'Se ha enviado correctamente tu correo.')
        return redirect('email')
        
