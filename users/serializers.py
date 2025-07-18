from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'auth0_id', 'nombre', 'telefono', 'direccion', 
                 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate(self, data):
        if self.instance and not data.get('nombre') and not self.instance.nombre:
            raise serializers.ValidationError("El nombre es requerido")
        return data