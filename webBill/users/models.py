from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(verbose_name = 'Email address', unique = True)
    REQUIRED_FIELDS = []
    nombre = models.CharField(verbose_name = 'Nombre', max_length = 40, blank = False)
    documento = models.CharField(verbose_name = 'Documento de identidad', max_length = 40, blank = False)
    institucion = models.CharField(verbose_name = 'Institución', max_length = 40, blank = False)
    direccion = models.CharField(verbose_name = 'Dirección', max_length = 40, blank = False)
    ciudad = models.CharField(verbose_name = 'Ciudad', max_length = 40, blank = False)
    telefono = models.CharField(verbose_name = 'Teléfono', max_length = 40, blank = False)
