from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from .validator import validar_rut

class CustomUserManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        """Crea y devuelve un usuario con un correo electrónico."""
        if not correo:
            raise ValueError('El correo electrónico debe ser proporcionado')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        """Crea y devuelve un superusuario con un correo electrónico."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractUser):
    TIPO_CUENTA_CHOICES = [
        ('normal', 'Normal'),
        ('admin', 'Administrador'),
    ]

    rut = models.CharField(max_length=10, validators=[validar_rut], unique=True)  # Haciendo el RUT único
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    celular = models.CharField(max_length=15)  
    tipo_cuenta = models.CharField(
        max_length=10,
        choices=TIPO_CUENTA_CHOICES,
        default='normal'
    )
   
    # Establece el campo de autenticación a 'correo'
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []  # No requiere campos adicionales para crear superusuarios

    objects = CustomUserManager()

    # Añadir related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios',  # Cambiado para evitar conflictos
        blank=True,
        help_text='Grupo de usuarios.',
        verbose_name='Grupos'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_permissions',  # Cambiado para evitar conflictos
        blank=True,
        help_text='Permisos específicos del usuario.',
        verbose_name='Permisos'
    )

    def __str__(self):
        return self.nombre


class Animal(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    edad = models.IntegerField()
    caracteristicas = models.TextField()
    disponible = models.BooleanField(default=True)  # Indica si el animal está disponible para adopción
    adoptado = models.BooleanField(default=False)  # Nuevo campo para indicar si el animal ha sido adoptado
    registrado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='animales_registrados')

    def __str__(self):
        return self.nombre


class SolicitudAdopcion(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    rut = models.CharField(max_length=10)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    animal_adoptado = models.BooleanField(default=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    mensaje = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Marcar como adoptado si la solicitud es aceptada
        if self.estado == 'aceptada':
            self.animal.disponible = False  # Marcar el animal como no disponible
            self.animal.adoptado = True  # Marcar el animal como adoptado
            self.animal.save()  # Guardar los cambios en el modelo Animal
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.estado}"
