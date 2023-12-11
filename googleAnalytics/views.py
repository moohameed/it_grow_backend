from rest_framework.decorators import api_view
from rest_framework.response import Response
from requests_oauthlib import OAuth2Session
from rest_framework import status
from django.shortcuts import redirect
import random
import string
import requests


# Define your OAuth 2.0 parameters
client_id = '568575930171-q1da2qt6f17pkblr2g8b95c9nu8dmqb6.apps.googleusercontent.com'  # Replace with your client ID
client_secret = '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'  # Replace with your client secret
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'http://localhost:8000/api/google-auth-callback'  # Replace with your redirect URI

@api_view(['GET'])
def google_auth(request):
    # Generate a random state and store it in the session
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    request.session['oauth2_state'] = state

    # Initialize OAuth 2.0 session for Google Analytics
    oauth2 = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=['https://www.googleapis.com/auth/analytics.readonly'])

    # Generate the authorization URL with the state
    authorization_url, _ = oauth2.authorization_url(authorization_base_url, state=state)

    return Response({"authorization_url": authorization_url})

@api_view(['GET'])
def google_auth_callback(request):
    state = request.GET.get("state")

    # Use the authorization code to get an access token
    code = request.GET.get("code")
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        # Now you have the access token for Google Analytics

        # Proceed to the next steps
        # You can store the access_token securely and use it for Google Analytics API requests
        react_app_url = f"http://localhost:3000/googleanalyticsproperties/?googleanalyticsaccestoken={access_token}"
        # return Response({"google_analytics_access_token": access_token})
        return redirect(react_app_url)
    else:
        # Handle the case where the token exchange was not successful
        
        return Response({"error": "Failed to obtain access token"})
    

@api_view(['GET'])
def google_analytics_properties(request):
    access_token = request.GET.get("access_token")
    
    if not access_token:
        print("Error: Access token is missing")
        return Response({"error": "Access token is missing"})  # Add Django REST framework response if needed

    def get_google_analytics_properties(access_token):
        # Define the API endpoints
        accounts_endpoint = 'https://www.googleapis.com/analytics/v3/management/accounts'
        webproperties_endpoint = 'https://www.googleapis.com/analytics/v3/management/accounts/{account_id}/webproperties'

        # Set up the headers with the access token
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        try:
            accounts_response = requests.get(accounts_endpoint, headers=headers)
            print("Accounts Response:", accounts_response.json())  # Add this print statement

            if accounts_response.status_code == 200:
                accounts_data = accounts_response.json()
                account_list = accounts_data.get('items', [])

                all_properties = []

                for account in account_list:
                    account_id = account.get('id')
                    webproperties_response = requests.get(
                        webproperties_endpoint.format(account_id=account_id),
                        headers=headers
                    )
                    print("Webproperties Response:", webproperties_response.json())  # Add this print statement

                    if webproperties_response.status_code == 200:
                        webproperties_data = webproperties_response.json()
                        webproperties = webproperties_data.get('items', [])
                        all_properties.extend(webproperties)

                return all_properties

            else:
                print("Error in accounts response:")
                print(accounts_response.content)
                return None

        except Exception as e:
            print("Error in accounts request:", str(e))
            return None

    properties = get_google_analytics_properties(access_token)

    if properties:
        response_data = [{"view_id": property['id'], "name": property['name']} for property in properties]
        print("Properties Data:", response_data)  # Add this print statement
        return Response(response_data)  # Add Django REST framework response if needed
    else:
        print("Failed to retrieve Google Analytics properties")
        return Response({"error": "Failed to retrieve Google Analytics properties"})  # Add Django REST framework response if needed
    

@api_view(['GET','POST'])
def google_analytics_data(request):
    access_token = request.data.get("access_token")
    selected_properties = request.data.get("selected_properties")
    print ("hello acces token" ,access_token)
    print ("hello selected prop" ,selected_properties)

    if not access_token:
        return Response({"error": "Access token is missing"})

    if not selected_properties:
        return Response({"error": "No properties selected"})

    # Define the same API endpoints for fetching properties
    accounts_endpoint = 'https://www.googleapis.com/analytics/v3/management/accounts'
    webproperties_endpoint = 'https://www.googleapis.com/analytics/v3/management/accounts/{account_id}/webproperties'

    # Set up the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    try:
        # Fetch data for the selected properties
        data = []

        for property_id in selected_properties:
            data_response = requests.get(f'{webproperties_endpoint.format(account_id=property_id)}', headers=headers)

            if data_response.status_code == 200:
                property_data = data_response.json()
                data.append(property_data)
            else:
                print(f"Error in fetching data for property {property_id}: {data_response.content}")

        return Response(data)
    except Exception as e:
        return Response({"error": f"Error fetching data: {str(e)}"})
