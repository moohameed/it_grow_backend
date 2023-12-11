from rest_framework import serializers
from .models import Person
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    # class Meta:
    #     model = Person 
    #     fields = '__all__'

    
    # def validate(self, data):

    #     special_caracter = "!@;:&é()"
    #     if any(c in special_caracter for c in data['name']):
    #         raise serializers.ValidationError('Name cannot contain the following characters : ! @ ; & é ( )')


    #     if data['age'] < 18:
    #         raise serializers.ValidationError('age should be more than 18')
        
    #     return data
    

    class Meta:
        model = User
        fields = ['id','username','password','email']
        