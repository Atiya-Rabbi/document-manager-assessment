from django.shortcuts import render

from rest_framework.response import Response
from propylon_document_manager.file_versions.api.controller import AuthController
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import FileVersion
from .serializers import FileVersionSerializer, UserSerializer

class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"


class RegisterViewSet(ViewSet):
    def post(self, request):
        controller = AuthController()
        user = controller.register(request.data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            if created:
               return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                })

        
        return Response(
            {'error': 'Invalid Data'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginViewSet(ViewSet):
    def post(self, request):
        controller = AuthController()
        user = controller.login(request.data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response(
            {'error': 'Invalid Credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )
