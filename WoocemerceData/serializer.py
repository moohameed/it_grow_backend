from rest_framework import serializers
from WoocemerceData.models import WooCommerceConnector
from django.contrib.auth.models import User

class WooSerializer(serializers.ModelSerializer):

    class Meta:
        model = WooCommerceConnector
        fields = '__all__'