from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    auth0_id = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
    
    def __str__(self):
        return f"{self.nombre} ({self.auth0_id})"