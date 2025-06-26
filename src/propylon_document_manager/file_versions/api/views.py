from django.shortcuts import render

from rest_framework.response import Response
from propylon_document_manager.file_versions.api.controller import AuthController
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import FileVersion
from .serializers import FileVersionSerializer, UserSerializer
from rest_framework.permissions import AllowAny

class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"


class RegisterViewSet(ViewSet):
    permission_classes = [AllowAny] 
    def create(self, request):
        controller = AuthController()
        user = controller.register(request.data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            if created:
               return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                },status=status.HTTP_201_CREATED)

        
        return Response(
            {'error': 'Invalid Data'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginViewSet(ViewSet):
    permission_classes = []
    def create(self, request):
        controller = AuthController()
        user = controller.login(request.data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            },status.HTTP_200_OK)
        
        return Response(
            {'error': 'Invalid Credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )

class LogoutViewSet(ViewSet):
    def create(self, request):
        request.user.auth_token.delete()
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )