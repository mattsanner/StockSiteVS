from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
from StockSite.settings import FERNET_KEY

# Create your models here.
class RobinhoodUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    token = models.BinaryField()
    signedin = models.BooleanField(default=False)
    # TODO: override setter to encrypt, getter to unencrypt
    def __str__(self):
        return self.username