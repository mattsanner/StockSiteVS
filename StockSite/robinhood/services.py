from django.db import models
import requests
from cryptography.fernet import Fernet
from django.conf import settings

from .models import RobinhoodUser

def encrypt_value(encrypt_me):
    f = Fernet(settings.FERNET_KEY)
    bitValue = bytes(encrypt_me, 'utf-8')
    return f.encrypt(bitValue)

class RobinhoodServices():
    def register(user, username, password): 
        r = requests.post('https://api.robinhood.com/api-token-auth/', {"username": username, "password": password})
        data = r.json()
        if 'token' in data.keys():
            rh_user = RobinhoodUser(user=user, username=username)
            rh_user.token = encrypt_value(data['token'])
            rh_user.signedin = True
            rh_user.save()            
            return True
        else:
            return False   #TODO log an error and possibly an error code/value in this case

    def authenticate(user, username, password):
        try:
            user.robinhooduser
            r = requests.post('https://api.robinhood.com/api-token-auth/', {"username": username, "password": password})
            data = r.json()
            if 'token' in data.keys():
                user.robinhooduser.token = encrypt_value(data['token'])
                user.robinhooduser.signedin = True
                user.robinhooduser.save()
        except RobinhoodUser.DoesNotExist as e:
            register(user, username, password)
        except Exception as e:
            return e
        
    def get_stocks(user):
        try:
            f = Fernet(settings.FERNET_KEY)
            key = f.decrypt(user.robinhooduser.token).decode("utf-8")
            r = requests.get("https://api.robinhood.com/accounts/", headers={"Authorization": ("Token " + key)})
            data = r.json()
            return data['portfolio']
        except Exception as e:
            return e

