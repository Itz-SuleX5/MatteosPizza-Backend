from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Ingrediente, Product
from .serializers import IngredienteSerializer, ProductSerializer

# INGREDIENTES VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ingrediente(request):
    serializer = IngredienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    serializer = IngredienteSerializer(ingredientes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ingrediente(request, pk):
    try:
        ingrediente = Ingrediente.objects.get(pk=pk)
        serializer = IngredienteSerializer(ingrediente)
        return Response(serializer.data)
    except Ingrediente.DoesNotExist:
        return Response({'error': 'Ingrediente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_ingrediente(request, pk):
    try:
        ingrediente = Ingrediente.objects.get(pk=pk)
        serializer = IngredienteSerializer(ingrediente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Ingrediente.DoesNotExist:
        return Response({'error': 'Ingrediente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ingrediente(request, pk):
    try:
        ingrediente = Ingrediente.objects.get(pk=pk)
        ingrediente.delete()
        return Response({'message': 'Ingrediente eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
    except Ingrediente.DoesNotExist:
        return Response({'error': 'Ingrediente no encontrado'}, status=status.HTTP_404_NOT_FOUND)


# PRODUCTOS VIEWS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # partial=True aquí
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
