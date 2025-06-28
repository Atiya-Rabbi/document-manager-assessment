from rest_framework import serializers

from ..models import File, FileVersion, User

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['url_path'] 
        
class FileVersionSerializer(serializers.ModelSerializer):
    url_path = serializers.CharField(source='file.url_path', read_only=True)
    
    class Meta:
        model = FileVersion
        fields = ['id', 'version_number', 'file_name', 'created_at', 'url_path']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True} 
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
