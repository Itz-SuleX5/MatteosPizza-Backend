from rest_framework import serializers
from .models import Order, OrderItem, UserProfile, Product
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    cantidad = serializers.IntegerField()
    precio_unitario = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'cantidad', 'precio_unitario', 'subtotal']

    def validate(self, data):
        print("=== ORDERITEMSERIALIZER VALIDATE ===")
        print(f"Item data received: {data}")
        print(f"Item data keys: {list(data.keys())}")
        
        # Validar que el producto existe
        if 'product' not in data:
            print("ERROR: 'product' key not found in item data")
            raise serializers.ValidationError("El campo 'product_id' es requerido")
            
        # Validar cantidad
        if 'cantidad' not in data:
            print("ERROR: 'cantidad' key not found in item data")
            raise serializers.ValidationError("El campo 'cantidad' es requerido")
            
        if data['cantidad'] <= 0:
            print(f"ERROR: Invalid cantidad: {data['cantidad']}")
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
            
        print(f"Item validation passed: product={data['product']}, cantidad={data['cantidad']}")
        return data

    def get_precio_unitario(self, obj):
        return str(obj.product.precio)

    def get_subtotal(self, obj):
        print(f"OrderItemSerializer: get_subtotal for product: {obj.product.nombre}, quantity: {obj.cantidad}, subtotal: {obj.product.precio * obj.cantidad}")
        return str(obj.product.precio * obj.cantidad)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_info = serializers.SerializerMethodField(read_only=True)
    estado = serializers.CharField()  # Hacer el campo menos restrictivo

    class Meta:
        model = Order
        fields = ['id', 'estado', 'metodo_pago', 'total', 'fecha_pedido', 'items', 'user_info']
        read_only_fields = ['total', 'fecha_pedido']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el estado opcional
        self.fields['estado'].required = False

    def validate(self, data):
        print("=== ORDERSERIALIZER VALIDATE ===")
        print(f"Data received in validate: {data}")
        print(f"Data keys: {list(data.keys())}")
        
        # Validar que items existe y no está vacío
        if 'items' not in data:
            print("ERROR: 'items' key not found in data")
            raise serializers.ValidationError("El campo 'items' es requerido")
        
        if not data['items']:
            print("ERROR: 'items' list is empty")
            raise serializers.ValidationError("Debe incluir al menos un item en la orden")
            
        print(f"Items received: {data['items']}")
        
        return data

    def get_user_info(self, obj):
        try:
            # Usar auth0_id para buscar en UserProfile
            perfil = UserProfile.objects.get(auth0_id=obj.auth0_user_id)
            return {
                'nombre': perfil.nombre,
                'direccion': perfil.direccion,
                'telefono': perfil.telefono,
            }
        except UserProfile.DoesNotExist:
            return {
                'nombre': '',
                'direccion': '',
                'telefono': ''
            }

    def create(self, validated_data, **kwargs):
        print("=== ORDERSERIALIZER CREATE ===")
        print(f"Validated data: {validated_data}")
        
        items_data = validated_data.pop('items')
        auth0_user_id = validated_data.get('auth0_user_id')
        
        print(f"Items data: {items_data}")
        print(f"Auth0 user ID: {auth0_user_id}")
        print(f"Remaining validated data: {validated_data}")
        
        # Crear la orden
        order = Order.objects.create(
            auth0_user_id=auth0_user_id,
            estado=validated_data.get('estado', 'Pendiente'),
            metodo_pago=validated_data.get('metodo_pago')
        )
        
        print(f"Order created with ID: {order.id}")

        # Crear los items y calcular el total
        total = 0
        for i, item_data in enumerate(items_data):
            print(f"Processing item {i}: {item_data}")
            
            product = item_data['product']
            cantidad = item_data['cantidad']
            subtotal = product.precio * cantidad
            total += subtotal
            
            print(f"Product: {product.nombre}, Precio: {product.precio}, Cantidad: {cantidad}, Subtotal: {subtotal}")

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                cantidad=cantidad
            )
            print(f"OrderItem created with ID: {order_item.id}")

        # Actualizar el total de la orden
        order.total = total
        order.save()
        
        # Refresh the order object to ensure related items are loaded
        order.refresh_from_db()
        
        print(f"Order total updated: {total}")
        print("=== ORDER CREATION COMPLETE ===")
        
        return order