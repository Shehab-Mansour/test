from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
import uuid

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if '@' in username:
            user_obj = get_object_or_404(users, email=username)
        else:
            user_obj = get_object_or_404(users, username=username)
        if check_password(password, user_obj.password):
            token_key = str(uuid.uuid4())
            token = CustomToken.objects.create(user=user_obj, key=token_key)
            return Response({'token': token.key , 'id': user_obj.id}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# @csrf_exempt
# @api_view(['POST'])
# def user_logout(request):
#     token_key = request.data.get('token')
#     if request.method == 'POST':
#         try:
#             token = get_object_or_404(CustomToken, key=token_key)
#             token.delete()
#             return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#


@csrf_exempt
@api_view(['POST'])
def user_logout(request):
    token_key = request.data.get('token')  # استرجاع التوكن من البيانات الواردة

    if request.method == 'POST':
        if not token_key:
            return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)  # التحقق من وجود التوكن

        try:
            token = get_object_or_404(CustomToken, key=token_key)  # البحث عن التوكن
            token.delete()  # حذف التوكن
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def newuserapi(request):
    user = users.objects.all()
    data = NewUserSerializer(user, many=True).data
    return Response({'data':data})



@api_view(['POST'])
def user_details(request):
    id = request.data.get('id')
    # print(id)
    try:
        user_obj = get_object_or_404(users, id=id)
        print("Fetched User:", user_obj)
        user_data = {
            'username': user_obj.username,
            "password" : user_obj.password,
            'email': user_obj.email,
            'birthday': user_obj.birthday,
            'state': user_obj.state,
        }
        return Response(user_data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
