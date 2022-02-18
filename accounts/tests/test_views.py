from django.test import TestCase, RequestFactory
from django.urls import reverse

from accounts.models import CustomUser
from accounts.views import SingupView

class SignUpViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )

    def test_signup(self):
        request = self.factory.get(reverse('signup'))
        request.user = self.user
        response = SingupView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('registration/signup.html'):
            response.render()
