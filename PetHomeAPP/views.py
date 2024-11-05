from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Animal, SolicitudAdopcion, Usuario
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroAnimalForm, RegistroUsuarioForm
from django.db import IntegrityError

def home(request):
    context = {
        'es_autenticado': request.user.is_authenticated,
        'es_admin': request.user.is_authenticated and request.user.tipo_cuenta == 'admin',
        'nombre_usuario': request.user.username if request.user.is_authenticated else '',
    }
    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, 'Has cerrado sesión correctamente.')  # Mensaje de éxito
    return redirect('home')  # Redirige a la página de inicio

def register_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.set_password(form.cleaned_data['password'])  # Establece la contraseña correctamente
            nuevo_usuario.username = form.cleaned_data['correo']  # Usa el correo proporcionado como username

            try:
                nuevo_usuario.save()
                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('login')  # Cambia 'login' por el nombre de tu vista de inicio de sesión
            except IntegrityError:
                messages.error(request, "El correo ya está en uso. Intenta con otro.")
        else:
            # Muestra errores en el formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')  # Captura el correo
        password = request.POST.get('password')  # Captura la contraseña

        # Autenticar con correo y contraseña
        user = authenticate(request, username=correo, password=password)
        if user is not None:
            login(request, user)  # Iniciar sesión si las credenciales son válidas
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')

    return render(request, 'login.html')  # Renderiza el formulario de inicio de sesión

@login_required
@user_passes_test(lambda u: u.tipo_cuenta == 'admin', login_url='home')
def admin_view(request):
    if request.method == 'POST':
        form = RegistroAnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.registrado_por = request.user
            animal.save()
            messages.success(request, 'Animal registrado correctamente.')
            return redirect('admin_view')
    else:
        form = RegistroAnimalForm()

    solicitudes = SolicitudAdopcion.objects.all()
    return render(request, 'admin_view.html', {
        'form': form,
        'solicitudes': solicitudes,
    })

def lista_animales(request):
    animales = Animal.objects.filter(disponible=True)  # Filtrar por animales disponibles
    return render(request, 'lista_animales.html', {'animales': animales})

@login_required
@user_passes_test(lambda u: u.tipo_cuenta == 'admin', login_url='home')
def registrar_animal(request):
    if request.method == 'POST':
        form = RegistroAnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.registrado_por = request.user  # Establece el usuario que registra
            animal.save()
            messages.success(request, 'Animal registrado correctamente.')
            return redirect('lista_animales')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = RegistroAnimalForm()
    return render(request, 'registrar_animal.html', {'form': form})

@login_required
def solicitar_adopcion(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    usuario = request.user
    nombre = usuario.get_full_name() or usuario.username
    correo = usuario.email
    telefono = getattr(usuario, 'celular', '')  # Usa 'celular' en vez de 'telefono'
    rut = getattr(usuario, 'rut', '')

    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '')  # Captura el mensaje del formulario
        try:
            solicitud = SolicitudAdopcion.objects.create(
                usuario=usuario,
                animal=animal,
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                rut=rut,
                estado='pendiente',  # Estado inicial 'pendiente'
                mensaje=mensaje
            )
            messages.success(request, 'Su solicitud de adopción ha sido enviada con éxito.')
            return redirect('lista_animales')
        except IntegrityError:
            messages.error(request, 'Ocurrió un error al enviar su solicitud. Inténtalo de nuevo.')
    
    context = {
        'animal': animal,
        'nombre': nombre,
        'correo': correo,
        'telefono': telefono,
        'rut': rut,
        'mensaje': ''  # Inicializar mensaje en el contexto
    }
    return render(request, 'solicitar_adopcion.html', context)

@login_required
@user_passes_test(lambda u: u.tipo_cuenta == 'admin', login_url='home')
def gestionar_solicitudes(request):
    solicitudes = SolicitudAdopcion.objects.all()
    return render(request, 'gestionar_solicitudes.html', {'solicitudes': solicitudes})

@login_required
@user_passes_test(lambda u: u.tipo_cuenta == 'admin', login_url='home')
def aceptar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=id)
    
    # Rechazar otras solicitudes del mismo animal
    SolicitudAdopcion.objects.filter(animal=solicitud.animal).exclude(id=id).update(estado='rechazada')
    
    # Aceptar la solicitud actual y marcar el animal como adoptado
    solicitud.estado = 'aceptada'
    solicitud.animal_adoptado = True
    solicitud.save()
    
    messages.success(request, 'Solicitud aceptada exitosamente. Recuerda contactar al usuario usando los datos proporcionados.')
    return redirect('gestionar_solicitudes')

@login_required
@user_passes_test(lambda u: u.tipo_cuenta == 'admin', login_url='home')
def rechazar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudAdopcion, id=id)
    solicitud.estado = 'rechazada'
    solicitud.save()
    messages.success(request, 'Solicitud rechazada exitosamente.')
    return redirect('gestionar_solicitudes')

@login_required
def mis_solicitudes(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirigir si el usuario no está autenticado

    solicitudes_activas = SolicitudAdopcion.objects.filter(usuario=request.user, estado='pendiente')
    solicitudes_historicas = SolicitudAdopcion.objects.filter(usuario=request.user).exclude(estado='pendiente')

    context = {
        'solicitudes_activas': solicitudes_activas,
        'solicitudes_historicas': solicitudes_historicas,
    }
    return render(request, 'mis_solicitudes.html', context)

def recuperar_contrasena(request):
    # Lógica para la recuperación de contraseña
    return render(request, 'recuperar_contrasena.html')

def exito_solicitud(request):
    return render(request, 'exito_solicitud.html')

def historial_solicitudes(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')  # Redirigir si no es admin

    solicitudes = SolicitudAdopcion.objects.all().order_by('-fecha_solicitud')  # Ordenar por fecha
    return render(request, 'historial_solicitudes.html', {'solicitudes': solicitudes})

@login_required
@user_passes_test(lambda u: u.tipo_cuenta == 'admin', login_url='home')
def marcar_como_adoptable(request, id):
    animal = get_object_or_404(Animal, id=id)
    animal.disponible = True
    animal.save()
    messages.success(request, 'El animal ha sido marcado nuevamente como adoptable.')
    return redirect('admin_view')
