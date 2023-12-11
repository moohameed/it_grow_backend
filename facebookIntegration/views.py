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

import urllib.parse

from django.http import JsonResponse
import json

@api_view(['GET'])
def facebook_login(request):
    redirect_uri = "https://187f-197-238-32-231.ngrok-free.app%s" % reverse('api:facebook_login')

    # Construct the OAuth URL
    oauth_url = "https://www.facebook.com/v12.0/dialog/oauth"
    oauth_params = {
        "client_id": "880730436914611",
        "redirect_uri": redirect_uri,
        "scope": "user_hometown,user_birthday,pages_show_list,read_insights",
    }
    oauth_url += "?" + urllib.parse.urlencode(oauth_params)

    if 'code' in request.GET:
        # Handle the code received from Facebook
        code = request.GET.get('code')
        print(f"Received code: {code}")

        access_token_url = 'https://graph.facebook.com/v12.0/oauth/access_token'
        access_token_params = {
            'client_id': "880730436914611",
            'client_secret': "20dac2a61b74fc61eec9e6ae7367f589",
            'code': code,
            'redirect_uri': redirect_uri,
        }
        response = requests.get(access_token_url, params=access_token_params)
        access_token_data = response.json()
        access_token = access_token_data.get("access_token")
        print(f"Access token data: {access_token_data}")
        print(f"Access token: {access_token}")

        # Fetch list of pages user manages
        pages_url = 'https://graph.facebook.com/v12.0/me/accounts'
        pages_data = requests.get(pages_url, params={'access_token': access_token}).json()
        print(f"Pages data: {pages_data}")

        # Redirecting to the React app with the pages data
        data_str = urllib.parse.quote(json.dumps({'page_data': pages_data['data']}))
        react_app_url = f"http://localhost:3000/facebook?data={data_str}"
        print(f"Redirecting to React app: {react_app_url}")
        return redirect(react_app_url)
    
    else:
        # Redirect the user to the OAuth URL to initiate the login flow
        print("Redirecting to Facebook OAuth")
        return redirect(oauth_url)


@api_view(['POST'])
def get_insights(request):
    try:
        page_id = request.data['page_id']
        access_token_for_page = request.data['access_token']
        metrics = request.data['metrics']

        insights_url = f'https://graph.facebook.com/v12.0/{page_id}/insights?metric={metrics}'
        insights_data = requests.get(insights_url, params={'access_token': access_token_for_page}).json()

        return Response(insights_data)
    except KeyError as e:
        return Response({"error": f"Key {e} not found in request data."}, status=400)
