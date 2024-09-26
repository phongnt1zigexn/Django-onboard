import pytest
from django.urls import reverse
from rest_framework import status
from snippets.models import Snippet
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    yield user
    user.delete()

@pytest.fixture
def api_client():
    return APIClient()

def create_new_snippet(client):
    url = '/snippets/' # Use reverse for URL resolution
    data = {'title': 'Test snippet', 'code': 'print("Hello, World!")', 'language': 'python'}
    return client.post(url, data, format='json')

@pytest.mark.django_db
def test_get_snippet_list(api_client):
    url = '/snippets/'
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_snippet_without_auth(api_client):
    response = create_new_snippet(api_client)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_create_snippet_with_basic_auth(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    response = create_new_snippet(api_client)
    assert response.status_code == status.HTTP_201_CREATED
