from logging import raiseExceptions

import pytest
from django.templatetags.i18n import language
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from snippets.serializers import SnippetSerializer
from snippets.models import Snippet
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def new_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    yield user
    user.delete()

@pytest.fixture
def new_snippet(db, new_user):
    snippet = Snippet.objects.create(title='test title', language='python', owner=new_user)
    yield snippet
    snippet.delete()

@pytest.fixture
def api_client():
    return APIClient()

def create_new_snippet(api_client):
    url = '/snippets/' # Use reverse for URL resolution
    data = {'title': 'Test snippet', 'code': 'print("Hello, World!")', 'language': 'python'}
    return api_client.post(url, data, format='json')

@pytest.mark.django_db
def test_get_snippet_details(api_client, new_snippet):
    url = f"/snippets/{new_snippet.id}/"
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'test title'
    assert response.data['language'] == 'python'
    assert response.data['owner'] == 'testuser'

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
def test_create_valid_snippet(api_client, new_user):
    api_client.force_authenticate(user=new_user)
    response = create_new_snippet(api_client)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_create_snippet_with_token_auth(api_client, new_user):
    token = Token.objects.create(user=new_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = create_new_snippet(api_client)
    assert response.status_code == status.HTTP_201_CREATED

def test_create_snippet_with_invalid_title(api_client, new_user):
    data = {'title': 'abc', 'language': 'python'}
    serializer = SnippetSerializer(data=data)
    with pytest.raises(ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
    assert 'must be greater than or equal to 5' in str(exc_info.value)