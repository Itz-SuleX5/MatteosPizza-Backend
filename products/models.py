from django.db import models
from django.utils import timezone

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'ingredientes'
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
    
    def __str__(self):
        return self.nombre

class Product(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.URLField(blank=True)
    ingredientes = models.ManyToManyField(Ingrediente, related_name='productos')
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    
    def __str__(self):
        return self.nombre