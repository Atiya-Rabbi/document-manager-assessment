import hashlib
import os
from sqlite3 import IntegrityError
from venv import logger
from django.shortcuts import render
from django.db import transaction

from rest_framework.response import Response
from propylon_document_manager.file_versions.api.controller import AuthController
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework import status
from ..models import ContentBlob, File, FileVersion
from .serializers import FileVersionSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FileVersionSerializer
    queryset = FileVersion.objects.all()
    lookup_field = "id"

    @action(detail=False, methods=['post'])
    def upload(self, request):
        try:
            """Handle file upload with versioning"""
            file_obj = request.FILES.get('file')
            desired_path = request.data.get('path')

            if not file_obj or not desired_path:
                return Response(
                    {'error': 'Both file and path are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            desired_path = desired_path.strip('/')
            content = file_obj.read()
            content_hash = hashlib.sha256(content).hexdigest()

            #get_or_create file_instance
            file_instance, _ = File.objects.get_or_create(
                url_path=desired_path,
                defaults={'owner': request.user}
            )

            # Check if identical content already exists
            existing_blob = ContentBlob.objects.filter(content_hash=content_hash).first()
            
            if existing_blob:
                # Content unchanged - get latest version
                current_version = file_instance.versions.first()
                return Response(
                    {
                        'warning': 'Content unchanged',
                        'version': FileVersionSerializer(current_version).data
                    },
                    status=status.HTTP_200_OK
                )

            # New content 
            with transaction.atomic():
                # Store in CAS
                content_blob = ContentBlob.objects.create(
                    content_hash=content_hash,
                    data=content,
                    size=len(content)
                )

                #create new_version
                new_version = FileVersion.objects.create(
                    file=file_instance,
                    version_number=file_instance.versions.count() + 1,
                    file_name=os.path.basename(file_obj.name),
                    content_blob=content_blob,
                    uploaded_by=request.user
                )

                file_instance.is_latest = True
                file_instance.save()

                return Response(
                    FileVersionSerializer(new_version).data,
                    status=status.HTTP_201_CREATED
                )
        
        except IntegrityError as e:
            return Response(
                {'error': f'Database error: {str(e)}'},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            logger.error(f"Upload failed: {str(e)}", exc_info=True)
            return Response(
                {'error': 'File processing failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

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