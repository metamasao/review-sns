from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware

from accounts.models import CustomUser
from accounts.views import SignupView


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class SignUpViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_signup_post(self):
        request = self.factory.post(
            reverse('accounts:signup'), 
            {
                'username':'testuser1', 
                'email':'testuser1@email.com', 
                'password1':'testpass123',
                'password2':'testpass123'
            }
        )
        request.user = AnonymousUser()
        add_middleware_to_request(request, SessionMiddleware)
        request.session.save()

        response = SignupView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        
        
