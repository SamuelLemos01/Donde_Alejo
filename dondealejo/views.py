from urllib import request
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
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

from .models import Producto, CarritoItem
def productos(request):
    producto_lista = Producto.objects.all()

    if request.method == "POST" and 'producto_id' in request.POST:
        producto_id = request.POST.get('producto_id')
        try:
            producto = Producto.objects.get(id=producto_id)
            
            if not request.user.is_authenticated:
                if not request.session.session_key:
                    request.session.create()
                sesion_id = request.session.session_key
                
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    sesion_id=sesion_id,
                    usuario=None
                )
                
                if not created:
                    carrito_item.cantidad += 1
                    carrito_item.save()
            else:
                carrito_item, created = CarritoItem.objects.get_or_create(
                    producto=producto,
                    usuario=request.user,
                    sesion_id=None
                )
                
                if not created:
                    carrito_item.cantidad += 1
                    carrito_item.save()
            
            messages.success(request, f"{producto.nombre} añadido al carrito")
        except Producto.DoesNotExist:
            messages.error(request, "Producto no encontrado")
    
    return render(request, 'menu.html', {'productos': producto_lista})


from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def restablecer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            enlace = request.build_absolute_uri(f"/cambiar_contrasena/{uid}/{token}/")
            send_mail(
                'Restablecer contraseña',
                f'Haz clic en el siguiente en enlace para restablecer tu contraseña {enlace}',
                'carenrojas212005@gmail.com',
                [email], 
                fail_silently=False
            )
            messages.success(request, "Se ah enviado un enlace de restablecimiento de contraseña a su correo")
            return redirect('login')
        else:
            messages.success(request, "No se encontro algun usuario registrado con ese correo")
        return redirect('restablecer')
    return render(request, 'email_restablecer.html')

def cambiar_contrasena(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            nueva_contrasena = request.POST.get("password")
            
            if not nueva_contrasena:
                messages.error(request, "La contraseña no puede estar vacía")
                return render(request, "email_contrasena.html")
                
            
            user.set_password(nueva_contrasena)
            user.save()
            
            return redirect('confirmacion_contrasena')
        
        return render(request, "email_contrasena.html")
    return redirect("login")

def confirmacion_contrasena(request):
    return render(request, "cambio_contrasena.html")


def home (request):
    return render(request, 'home.html')

def perfil (request):
    return render(request, 'perfil.html')

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



def contacto (request):
    return render(request, 'contacto.html')



from django.shortcuts import render
from django.conf import settings

def contacto_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Configuración del correo
        subject = f"Nuevo mensaje de {name}"
        body = f"Mensaje de: {name}\nCorreo: {email}\n\nMensaje:\n{message}"
        recipient_email = 'carenrojas212005@gmail.com'  # Correo del propietario

        # Enviar el correo
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient_email])

        # Renderizar la página con el mensaje de éxito
        return render(request, 'contacto.html', {'success': True})

    return render(request, 'contacto.html')

def ver_carrito(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    for item in carrito_items:
        total += item.subtotal()
    
    return render(request, 'carrito.html', {
        'carrito_items': carrito_items,
        'total': total
    })

def actualizar_carrito(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()
            
            messages.success(request, "Carrito actualizado")
        else:
            messages.error(request, "No tienes permiso para modificar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

def eliminar_item(request, item_id):
    try:
        item = CarritoItem.objects.get(id=item_id)
        
        if request.user.is_authenticated and item.usuario == request.user or \
            not request.user.is_authenticated and item.sesion_id == request.session.session_key:
            
            item.delete()
            messages.success(request, "Item eliminado del carrito")
        else:
            messages.error(request, "No tienes permiso para eliminar este item")
    except CarritoItem.DoesNotExist:
        messages.error(request, "Item no encontrado")
        
    return redirect('ver_carrito')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoItem, Orden, OrdenItem
from .forms import OrdenForm
from .models import Datos
def pasarela(request):
    carrito_items = []
    total = 0
    
    if request.user.is_authenticated:
        carrito_items = CarritoItem.objects.filter(usuario=request.user)
    else:
        if request.session.session_key:
            carrito_items = CarritoItem.objects.filter(sesion_id=request.session.session_key)
    
    if not carrito_items:
        messages.warning(request, "Tu carrito está vacío")
        return redirect('ver_carrito')
    
    for item in carrito_items:
        total += item.subtotal()
    
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit=False)
            
            if request.user.is_authenticated:
                orden.usuario = request.user
            else:
                orden.sesion_id = request.session.session_key
            
            orden.total = total
            orden.save()
            
            for item in carrito_items:
                OrdenItem.objects.create(
                    orden=orden,
                    producto=item.producto,
                    precio=item.producto.precio,
                    cantidad=item.cantidad
                )
            
            carrito_items.delete()
            
            messages.success(request, "Tu pedido ha sido procesado con éxito")
            return redirect('confirmacion', orden_id=orden.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            try:
                datos = Datos.objects.get(user=request.user)
                initial_data = {
                    'nombre': f"{datos.nombre} {datos.apellido}",
                    'email': request.user.email
                }
            except Datos.DoesNotExist:
                initial_data = {
                    'nombre': request.user.username,
                    'email': request.user.email
                }
        
        form = OrdenForm(initial=initial_data)
    
    return render(request, 'pasarela.html', {
        'form': form,
        'carrito_items': carrito_items,
        'total': total
    })

def confirmacion(request, orden_id):
    try:
        if request.user.is_authenticated:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        else:
            orden = Orden.objects.get(id=orden_id, sesion_id=request.session.session_key)
        
        items = OrdenItem.objects.filter(orden=orden)
        
        return render(request, 'confirmacion.html', {
            'orden': orden,
            'items': items
        })
    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada")
        return redirect('productos')