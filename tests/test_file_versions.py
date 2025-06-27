from django.urls import reverse
from propylon_document_manager.file_versions.models import FileVersion, ContentBlob

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from .factories import FileVersionFactory, UserFactory, FileFactory

from django.core.files.uploadedfile import SimpleUploadedFile

class FileUploadTests(APITestCase):
    def setUp(self):
        password = 'testpass123'
        # Create test user and token
        self.user = UserFactory(password=password)  
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.file = FileFactory(url_path="/documents/test.pdf")
        self.test_file = SimpleUploadedFile(
            "test.pdf", 
            b"file_content", 
            content_type="application/pdf"
        )
        
        self.url = reverse('api:fileversion-upload')  

    def test_authenticated_upload(self):
        """Test successful authenticated upload"""
        response = self.client.post(
            self.url,
            {'file': self.test_file, 'path': self.file.url_path},
            format='multipart'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(FileVersion.objects.exists())
        self.assertTrue(ContentBlob.objects.exists())
    
    def test_duplicate_content_upload(self):
        """Test uploading identical content doesn't create new blob"""
        # First upload
        self.client.post(self.url, {
            'file': self.test_file, 
            'path': self.file.url_path
        }, format='multipart')
        
        # Second upload with same content
        same_file = SimpleUploadedFile(
            "test_copy.pdf", 
            b"file_content",  # Same content
            content_type="application/pdf"
        )
        response = self.client.post(
            self.url,
            {'file': same_file, 'path': self.file.url_path},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, 200)  # return existing version
        self.assertEqual(ContentBlob.objects.count(), 1)  # Only one blob stored

    def test_file_versions(self):
        """Test version numbers increment correctly"""
        # v1
        self.client.post(self.url, {
            'file': self.test_file, 
            'path': self.file.url_path
        }, format='multipart')
        
        # v2
        new_file = SimpleUploadedFile(
            "test_v2.pdf", 
            b"new_content", 
            content_type="application/pdf"
        )
        response = self.client.post(
            self.url,
            {'file': new_file, 'path': self.file.url_path},
            format='multipart'
        )
        self.assertEqual(response.data['version_number'], 2)

    def test_unauthenticated_upload(self):
        """Test upload without token fails"""
        self.client.credentials()  # Clear auth
        response = self.client.post(
            self.url,
            {'file': self.test_file, 'path': self.file.url_path},
            format='multipart'
        )
        self.assertEqual(response.status_code, 401)