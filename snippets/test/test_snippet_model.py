import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from snippets.models import Snippet
from rest_framework.test import APIClient
from django.contrib.auth.models import User

def create_new_snippet(client):
    url = '/snippets/'
    data = {'title': 'Test snippet', 'code': 'print("Hello, World!")', 'language': 'python'}
    return client.post(url, data, format='json')

class TestSnippets(APITestCase):
    def test_get_snippet_list(self):
        url = '/snippets/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_create_snippet_without_auth(self):
        response = create_new_snippet(self.client)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.django_db
    def test_create_snippet_with_basic_auth(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        response = create_new_snippet(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
