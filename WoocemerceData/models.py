from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WooCommerceConnector(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_url = models.URLField(max_length=200)
    consumer_key = models.CharField(max_length=200)
    consumer_secret = models.CharField(max_length=200)