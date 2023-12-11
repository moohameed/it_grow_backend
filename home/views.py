from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from home.models import Person
from home.serializer import UserSerializer
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator 
from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404 
from home.config import ACCESS_TOKEN

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from urllib.parse import urlencode  # Import urlencode from urllib.parse


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User , username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response ({"detail" : "not found ! "}, status=status.HTTP_404_NOT_FOUND)
    token , created  = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance = user)
    return Response({"token": token.key , "user": serializer.data})


@api_view(['POST'])
def signup(request):
    # return Response({"detail": "User registered successfully. Check your email for verification instructions."})
    # print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.is_active = False  # Mark user as inactive until email is verified
        user.save()

        # Generate a verification token
        token = Token.objects.create(user=user)
        current_site = get_current_site(request).domain
        # Send email with verification link
        verification_link = 'http://' + current_site + '/api/verify_email/' + str(token)
        subject = "Verify your email"
        message = f"Click the following link to verify your email: {verification_link}"
        send_mail(subject, message, "noreply@yourdomain.com", [user.email])

        return Response({"detail": "User registered successfully. Check your email for verification instructions."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def verify_email(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        if user.is_active:
            return Response({'message': 'Email already verified', 'user': None})

        user.is_active = True
        user.save()
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token
            # Add more fields as needed
        }
        return Response({'message': 'Email verified', 'user': user_data})
    except Token.DoesNotExist:
        return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def test_token(request):
    return Response({})

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=204)
    

def generate_reset_token(user):
    return default_token_generator.make_token(user)



@api_view(['POST'])
def send_reset_email(request):
    pk = request.data.get('user')
    utilisateur = User.objects.get(id=pk)
    token = Token.objects.get(user_id=pk)
    tokenn = token.key
    try:
        
       
        current_site = get_current_site(request).domain
        # Send email with verification link
        verification_link = 'http://' + current_site + '/api/reset_password/'+str(tokenn)
        subject = "Password Reset"
        message = f"Click the following link to reset your password: {verification_link}"
        send_mail(subject, message, "noreply@yourdomain.com", [utilisateur.email])
        return Response({'message': 'Password reset email sent successfully.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def reset_password(request,tokenn):
    try:

        token = Token.objects.get(key=tokenn)
        idu = token.user_id
        user = User.objects.get(id=idu)

            # Token is valid, display a form for password reset
        if request.method == 'POST':
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully.'})
        else:
            return Response({'message': 'Please enter your new password.'})

    
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)








