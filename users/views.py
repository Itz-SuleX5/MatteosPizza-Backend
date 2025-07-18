from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .models import UserProfile
from .serializers import UserProfileSerializer

def handle_error(message, status_code=400):
    return JsonResponse({'error': message}, status=status_code)

@api_view(['POST'])
def create_user_profile(request):
    try:
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return handle_error(f"Error interno: {str(e)}", 500)

@api_view(['GET'])
def list_users(request):
    try:
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return handle_error(f"Error al obtener usuarios: {str(e)}", 500)

@api_view(['GET'])
def get_user_profile(request, auth0_id):
    try:
        user = UserProfile.objects.get(auth0_id=auth0_id)
        serializer = UserProfileSerializer(user)
        response_data = serializer.data.copy()
        response_data['address'] = response_data.get('direccion', '')
        response_data['phone'] = response_data.get('telefono', '')
        return Response(response_data)
    except UserProfile.DoesNotExist:
        return handle_error('Usuario no encontrado', 404)
    except Exception as e:
        return handle_error(f"Error interno: {str(e)}", 500)

@api_view(['POST', 'PUT', 'PATCH'])
def create_or_update_profile(request):
    try:
        auth0_id = request.data.get('auth0_id')
        if not auth0_id:
            return handle_error('auth0_id es requerido', 400)

        try:
            user = UserProfile.objects.get(auth0_id=auth0_id)
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_instance = serializer.save()
                # 🔥 Aquí usamos serializer.data porque refleja exactamente lo que se guardó
                response_data = serializer.data.copy()
                response_data['address'] = response_data.get('direccion', '')
                response_data['phone'] = response_data.get('telefono', '')
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            # Si no existe, lo creamos desde cero
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                new_instance = serializer.save()
                response_data = serializer.data.copy()
                response_data['address'] = response_data.get('direccion', '')
                response_data['phone'] = response_data.get('telefono', '')
                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return handle_error(f"Error interno: {str(e)}", 500)




@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    try:
        if request.method == 'GET':
            auth0_id = request.GET.get('auth0_id') or request.headers.get('X-Auth0-ID')
            if not auth0_id:
                return handle_error('auth0_id es requerido', 400)
            try:
                user = UserProfile.objects.get(auth0_id=auth0_id)
                serializer = UserProfileSerializer(user)
                response_data = serializer.data.copy()
                response_data['address'] = response_data.get('direccion', '')
                response_data['phone'] = response_data.get('telefono', '')
                return Response(response_data)
            except UserProfile.DoesNotExist:
                return handle_error('Usuario no encontrado', 404)
        elif request.method in ['POST', 'PUT', 'PATCH']:
            return create_or_update_profile(request)
    except Exception as e:
        return handle_error(f"Error interno: {str(e)}", 500)
