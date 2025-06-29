import hashlib
import os
from sqlite3 import IntegrityError
from venv import logger
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import FileResponse, Http404, HttpResponse
from rest_framework.response import Response
from propylon_document_manager.file_versions.api.controller import AuthController
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework import status
from urllib.parse import unquote
from ..models import ContentBlob, File, FileVersion
from .serializers import FileVersionSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication


class FileVersionViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FileVersionSerializer
    lookup_field = "id"

    def get_queryset(self):
        """
        Return only FileVersions where:
        1. The file is owned by the current user
        2. The file version is the latest (is_latest=True)
        """
        
        return FileVersion.objects.filter(
            file__owner=self.request.user,
            is_latest=True
        ).select_related('file', 'content_blob')
    
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
            file_instance, created = File.objects.get_or_create(
                url_path=desired_path,
                owner=request.user,  
                defaults={'owner': request.user}
            )

            # Check if identical content already exists
            #existing_blob = ContentBlob.objects.filter(content_hash=content_hash).first()
            # Check for existing content IN THIS USER'S FILE
            existing_version = FileVersion.objects.filter(
                file__owner=request.user,
                file__url_path=desired_path,
                content_blob__content_hash=content_hash
            ).order_by('-version_number').first()
            
            if existing_version and not created:
                # Content unchanged - get latest version
                #current_version = file_instance.versions.first()
                return Response(
                    {
                        'warning': 'Content unchanged',
                        'version': FileVersionSerializer(existing_version).data
                    },
                    status=status.HTTP_200_OK
                )

            # New content 
            with transaction.atomic():
                #Set all previous versions to is_latest=False
                file_instance.versions.update(is_latest=False)
                
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
                    uploaded_by=request.user,
                    is_latest = True
                )

                # file_instance.is_latest = True
                # file_instance.save()

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

    @action(detail=False, methods=['get'], url_path='retrieve/(?P<path>[^/].*)')
    def retrieve_files(self, request, path=None):
        """
        Retrieve file by path with optional version parameter.
        URL format: /api/file_versions/retrieve/<path>?revision=<int>
        """
        
        try:
            # Decode URL-encoded path
            normalized_path = unquote(path).lstrip('/')
            print(f"Searching for path: {normalized_path}") 
            # Get the file (ensure owner matches requesting user)
            file_obj = get_object_or_404(
                File,
                url_path=normalized_path,
                owner=request.user  # Critical security check
            )
            print(f"FILE OBJECT--------- {file_obj}")
            # Get specific revision or latest
            revision = request.query_params.get('revision')

            if revision:
                version = get_object_or_404(
                    file_obj.versions.all(),
                    version_number=int(revision)+1
                )
                if not version:
                    raise Http404("No versions exist for this file")
            else:
                version = file_obj.versions.order_by('-version_number').first()
            
                if not version:
                    raise Http404("No versions exist for this file")
            
        
            # Get file extension and set content type
            file_ext = version.file_name.split('.')[-1].lower()
            content_type = {
                # Documents
                'pdf': 'application/pdf',
                'txt': 'text/plain',
                'html': 'text/html',
                'htm': 'text/html',
                'csv': 'text/csv',
                
                # Images
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'svg': 'image/svg+xml',  # Fixed MIME type
                'webp': 'image/webp',
                'ico': 'image/x-icon',
                'bmp': 'image/bmp',
            }.get(file_ext, 'application/octet-stream')
            
            response = HttpResponse(version.content_blob.data, content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{version.file_name}"'
            return response
                    
        except Http404:
            return Response(
                {"error": "File not found or access denied"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
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