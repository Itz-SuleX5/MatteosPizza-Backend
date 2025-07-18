from rest_framework import serializers
from .models import Ingrediente, Product

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre', 'descripcion', 'disponible']

class ProductSerializer(serializers.ModelSerializer):
    ingredientes_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    ingredientes = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen_url', 
                 'ingredientes_ids', 'ingredientes', 'disponible']
    
    def create(self, validated_data):
        ingredientes_ids = validated_data.pop('ingredientes_ids', [])
        product = Product.objects.create(**validated_data)
        
        if ingredientes_ids:
            ingredientes = Ingrediente.objects.filter(id__in=ingredientes_ids)
            product.ingredientes.set(ingredientes)
        
        return product
    
    def update(self, instance, validated_data):
        ingredientes_ids = validated_data.pop('ingredientes_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if ingredientes_ids is not None:
            ingredientes = Ingrediente.objects.filter(id__in=ingredientes_ids)
            instance.ingredientes.set(ingredientes)
        
        return instance