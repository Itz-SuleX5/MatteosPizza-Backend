from django.db import models
from django.utils import timezone
from products.models import Product
from users.models import UserProfile

class Order(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'Preparando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    auth0_user_id = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    metodo_pago = models.CharField(max_length=50, default='Efectivo')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_pedido = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.auth0_user_id}"
    
    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(blank=True)
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def save(self, *args, **kwargs):
        self.precio_unitario = self.product.precio
        self.subtotal = self.precio_unitario * self.cantidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cantidad}x {self.product.nombre}"