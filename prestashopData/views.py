from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from prestashopData.models import PrestaShopConnector
from prestashopData.connector import PrestaShopManager
from prestashopData.serializer import PrestashopSerializer
from django.contrib.auth.models import User
import json
import traceback




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prestashop_orders(request):
    try:
        # Assuming you have only one PrestashopConnector object per user
        connector = PrestaShopConnector.objects.filter(user=request.user).first()
        if not connector:
            return Response({'message': 'No Prestashop connector found for this user.'}, status=400)
        
        manager = PrestaShopManager(connector.api_url, connector.api_key)
        orders = manager.get_orders()
        
        return Response(orders)
        
    except Exception as e:
        print(e)  # Print the error to the console.
        print(traceback.format_exc())  # This will print detailed traceback.
        return Response({'message': str(e)}, status=500)


### Get all credentials #####
@api_view(['GET'])
def presta_list(request):
    users = PrestaShopConnector.objects.all()
    serializer = PrestashopSerializer(users, many=True)
    return Response(serializer.data)


### create credtial credentials #####
@api_view(['POST'])
def presta_create(request):
    serializer = PrestashopSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
