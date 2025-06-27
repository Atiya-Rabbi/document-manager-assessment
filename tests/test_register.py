from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


client = APIClient()

def test_register_success():
    url = reverse('api:register-list')
    valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        
    response = client.post(url, valid_data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert 'token' in response.data

    user_data = response.data['user']
    assert user_data['email'] == 'test@example.com'
    assert user_data['name'] == 'Test User'
    assert 'password' not in user_data


def test_register_invalid_data():
    url = reverse('api:register-list')
    data = {
            'name': 'Test User',
            'email': 'test.com',
            'password': 'short'
        }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST