from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PrestaShopConnector(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_url = models.URLField(max_length=200)
    api_key = models.CharField(max_length=200)
