from propylon_document_manager.file_versions.api.serializers import UserSerializer
from django.contrib.auth import authenticate


class AuthController:
    serializer_class = UserSerializer
    
    def register(self, data):
        user = data.save()
        return user
        
    def login(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        return user
