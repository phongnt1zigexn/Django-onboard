import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from snippets.models import Snippet
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def new_user(db):
	user = User.objects.create_user(username='testuser', password='testpassword')
	yield user
	user.delete()

@pytest.fixture
def api_client():
	return APIClient()

@pytest.mark.django_db
def test_generate_token(api_client, new_user):
	response = api_client.post('/account/login/', {'username': 'testuser', 'password': 'testpassword'})
	assert response.data['token'] is not None