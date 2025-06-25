from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status


class AuthController:
    def register(self, data):
        user = data.save()
        token, created = Token.objects.get_or_create(user=user)
        if created:
            #something
            return 200
        
    def login(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return 200
        return 400
