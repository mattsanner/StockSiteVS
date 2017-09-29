from django.db import models
import requests

from .models import RobinhoodUser

class RobinhoodServices():
    def authenticate(user, username, password):
        r = requests.post('https://api.robinhood.com/api-token-auth/', {"username": username, "password": password})
        data = r.json()
        if 'token' in data.keys():
            rh_user = RobinhoodUser(user=user, username=username)
            rh_user.token = data['token']
            rh_user.save()            
            return True
        else:
            return False   #TODO log an error and possibly an error code/value in this case

    def register(user, username, password):           
        """if user.robinhooduser.exists:
            raise LookupError("User already has Robinhood user. Only allowed to register account once currently.")
            return False"""
        if RobinhoodServices.authenticate(user, username, password):            
            return True
        else:
            raise Exception("An error occured while authenticating or saving robinhooduser data to user")
        
    def get_stocks(username):
        r = requests
