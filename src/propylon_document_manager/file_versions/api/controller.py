from propylon_document_manager.file_versions.api.serializers import UserSerializer
from django.contrib.auth import authenticate


class AuthController:

    def register(self, data):
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()  
            return user
        
        print("Registration errors:", serializer.errors) 
        return None
        
    def login(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        return user
