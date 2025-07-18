from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    # Log de los datos recibidos
    logger.info("=== CREATE ORDER DEBUG ===")
    logger.info(f"Request data: {request.data}")
    logger.info(f"Request user: {request.user}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    print("=== CREATE ORDER DEBUG ===")
    print(f"Request data: {request.data}")
    print(f"Request user: {request.user}")
    print(f"Data type: {type(request.data)}")
    
    # Mostrar estructura esperada
    expected_structure = {
        'auth0_user_id': 'string',
        'estado': 'string',
        'metodo_pago': 'string',
        'items': [
            {
                'product_id': 'integer',
                'cantidad': 'integer'
            }
        ]
    }
    print(f"Expected structure: {expected_structure}")
    
    serializer = OrderSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            print("Serializer is valid, creating order...")
            order = serializer.save(auth0_user_id=request.user.auth0_id)
            
            # Serializar la orden creada para la respuesta
            response_serializer = OrderSerializer(order)
            
            print(f"Order created successfully with ID: {order.id}")
            print(f"Response data being sent: {response_serializer.data}")
            
            return Response({
                'success': True,
                'message': 'Orden creada exitosamente',
                'order': response_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error creating order: {str(e)}")
            logger.error(f"Error creating order: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error al crear la orden: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Log detallado de errores de validación
    print("=== VALIDATION ERRORS ===")
    print(f"Serializer errors: {serializer.errors}")
    
    # Mostrar errores por campo
    for field, errors in serializer.errors.items():
        print(f"Field '{field}': {errors}")
    
    logger.error(f"Validation errors: {serializer.errors}")
    
    return Response({
        'success': False,
        'message': 'Datos inválidos',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    orders = Order.objects.all().order_by('-fecha_pedido')
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    auth0_user_id = request.user.auth0_id
    orders = Order.objects.filter(auth0_user_id=auth0_user_id).order_by('-fecha_pedido')
    serializer = OrderSerializer(orders, many=True)
    # Capitaliza el campo 'estado' para cada pedido
    pedidos = serializer.data
    for pedido in pedidos:
        if 'estado' in pedido and isinstance(pedido['estado'], str):
            pedido['estado'] = pedido['estado'].capitalize()
    return Response({'orders': pedidos})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    nuevo_estado = request.data.get('estado', '').capitalize()  # Primera letra mayúscula

    # Validamos que el nuevo estado exista en las opciones del campo 'estado' del modelo
    estados_validos = [choice[0].capitalize() for choice in order._meta.get_field('estado').choices]

    if nuevo_estado not in estados_validos:
        return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

    order.estado = nuevo_estado
    order.save()
    return Response({'status': 'success', 'order': {'id': order.id, 'estado': order.estado}})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)