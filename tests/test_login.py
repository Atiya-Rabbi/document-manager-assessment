from django.urls import reverse
from propylon_document_manager.file_versions.models import User
from rest_framework import status
from rest_framework.test import APIClient


client = APIClient()

def test_login_success():
    user_data = {
        'email': 'test@example.com',
        'password': 'testpass123',
        'name': 'Test User'
    }
    User.objects.create_user(**user_data)
    
    url = reverse('api:login-list')
    response = client.post(url, {
        'email': 'test@example.com',
        'password': 'testpass123'
    }, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert 'user' in response.data
    assert response.data['user']['email'] == 'test@example.com'
    assert 'password' not in response.data['user']


def test_login_failure_wrong_password():
    # Create test user
    User.objects.create_user(
        email='test@example.com',
        password='correctpass',
        name='Test User'
    )
    
    url = reverse('api:login-list')
    response = client.post(url, {
        'email': 'test@example.com',
        'password': 'wrongpass'
    }, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data
    assert response.data['error'] == 'Invalid Credentials'
