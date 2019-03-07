from django.test import TestCase
from django.utils.http import urlencode
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate
from .models import Session
from . import views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Create your tests here.
class LoginTest(APITestCase):

    def test_get_token_login_valid_username_and_password(self):
        client = APIClient()
        user = User.objects.create_user(
            'usertest', 'user01@example.com', 'usertestP4ssw0rD')

        token = Token.objects.create(user=user)

        data = {
            'username': 'usertest',
            'password': 'usertestP4ssw0rD', }

        response = client.post(
            'http://localhost:8000/sessions/login', data=data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_get_token_login_invalid_username_and_password(self):
        client = APIClient()

        data = {
            'username': 'usertest',
            'password': 'usertestP4ssw0rD', }

        response = client.post(
            'http://localhost:8000/sessions/login', data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class RunningSessionTest(APITestCase):

    def test_get_sessions(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_sessions_not_authenticated_user(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        request = factory.get('http://localhost:8000/sessions/')
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_new_session(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.post('http://localhost:8000/sessions/', data=data)
        force_authenticate(request, user=user)
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_new_session_not_authenticated_user(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.post('http://localhost:8000/sessions/', data=data)
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_specific_speed_authenticated(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        # create new running session:
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)

        request = factory.get('http://localhost:8000/sessions/{session.pk}')
        force_authenticate(request, user=user)
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_specific_speed_unauthenticated(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        # create new running session:
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)

        request = factory.get('http://localhost:8000/sessions/{session.pk}')
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_avg_speed_authenticated(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        # create new running session:
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)

        request = factory.get('http://localhost:8000/sessions/averagespeed')
        force_authenticate(request, user=user)
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_avg_speed_unauthenticated(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        # create new running session:
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)

        request = factory.get('http://localhost:8000/sessions/averagespeed')
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_total_distance_authenticated(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        # create new running session:
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)

        request = factory.get('http://localhost:8000/sessions/totaldistance')
        force_authenticate(request, user=user)
        response = view(request)
        assert response.status_code == status.HTTP_200_OK

    def test_get_total_distance_unauthenticated(self):
        factory = APIRequestFactory()
        view = views.SessionList.as_view()
        user = User.objects.create_user(
            'user01', 'user01@example.com', 'user01P4ssw0rD')

        # create new running session:
        session = Session(distance_in_miles=10.0, length_of_run=1.0)
        data = {
            "distance_in_miles": [session.distance_in_miles
                                  ],
            "length_of_run": [session.length_of_run
                              ]
        }

        request = factory.get('http://localhost:8000/sessions/')
        force_authenticate(request, user=user)

        request = factory.get('http://localhost:8000/sessions/totaldistance')
        response = view(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
