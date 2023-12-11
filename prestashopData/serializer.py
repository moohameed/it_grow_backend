from rest_framework import serializers
from prestashopData.models import PrestaShopConnector
from django.contrib.auth.models import User

class PrestashopSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrestaShopConnector
        fields = '__all__'