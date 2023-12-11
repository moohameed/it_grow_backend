from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from WoocemerceData.models import WooCommerceConnector
from WoocemerceData.connector import WooCommerceManager
from WoocemerceData.serializer import WooSerializer
from django.contrib.auth.models import User
import pdb
from rest_framework import status



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def woocommerce_orders(request):
    try:
        # Retrieve all WooCommerceConnector objects for the authenticated user
        connectors = WooCommerceConnector.objects.filter(user=request.user)
        
        if not connectors:
            return Response({'message': 'No WooCommerceConnector found for this user.'}, status=400)
        
        if connectors.count() <= 2:
            # If there are 2 or fewer connectors, proceed with fetching orders
            manager = WooCommerceManager(connectors.first().api_url, connectors.first().consumer_key, connectors.first().consumer_secret)
            orders = manager.get_orders()
            
            if 'code' in orders and orders['code'] == 'rest_no_route':
                return Response({'message': 'Could not find route on the server. Please check your WooCommerce setup.'}, status=400)
            
            return Response(orders)
        else:
            # If there are more than 2 connectors, return a list of user IDs connected
            user_ids_connected = [connector.id for connector in connectors]
            return Response({'message': 'More than 2 woocommerce connected', 'user_ids_connected': user_ids_connected})
        
    except Exception as e:
        print(e)  # Print the error to the console.
        return Response({'message': str(e)}, status=500)



#I use this one in the frontend
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def woocommerce_orders_unique(request,pk):
    try:
        # Assuming you have only one WooCommerceConnector object per user
        connector = WooCommerceConnector.objects.get(id=pk)
        if not connector:
            return Response({'message': 'No WooCommerceConnector found '}, status=400)
        
        manager = WooCommerceManager(connector.api_url, connector.consumer_key, connector.consumer_secret)
        orders = manager.get_orders()
        
        if 'code' in orders and orders['code'] == 'rest_no_route':
            return Response({'message': 'Could not find route on the server. Please check your WooCommerce setup.'}, status=400)
        
        return Response(orders)
        
    except Exception as e:
        print(e)  # Print the error to the console.
        return Response({'message': str(e)}, status=500) 

    
### Get all credentials #####
@api_view(['GET'])
def woo_list(request):
    users = WooCommerceConnector.objects.all()
    serializer = WooSerializer(users, many=True)
    return Response(serializer.data)


### create credtial credentials #####
#I use this one in the frontend
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def woo_create(request):
    data = request.data.copy()  # Making a shallow copy so we can add the user to it
    data["user"] = request.user.id  # Assign the logged-in user's ID to the data
    serializer = WooSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

### Get user related credentials #####
#I use this one in the frontend
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def woo_user(request):
    # Directly get the WooCommerceConnectors related to the currently authenticated user
    connectors = request.user.woocommerceconnector_set.all()
    serializer = WooSerializer(connectors, many=True)
    return Response(serializer.data)



#I use this one in the frontend
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def woo_delete(request, pk):
    try:
        connector = WooCommerceConnector.objects.get(pk=pk)
        
        # Ensure that the connector belongs to the currently authenticated user
        if connector.user != request.user:
            return Response({'message':'Unauthorized action.'}, status=status.HTTP_403_FORBIDDEN)

    except WooCommerceConnector.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    connector.delete()
    return Response({'message':'WooCommerce connector deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

