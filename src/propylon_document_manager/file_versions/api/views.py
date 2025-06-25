from django.shortcuts import render

from rest_framework.response import Response
from propylon_document_manager.file_versions.api.controller import AuthController
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from ..models import FileVersion
from .serializers import FileVersionSerializer

class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"


class RegisterViewSet(ViewSet):
    def post(self, request):
        controller = AuthController()
        status = controller.register(request.data)
        #did the user register?
        return Response({'success'
            },status=status.HTTP_200)


class LoginViewSet(ViewSet):
    def post(self, request):
        controller = AuthController()
        status = controller.login(request.data)
        #did the user login successfully?
        return Response({'success'
            },status=status.HTTP_200)