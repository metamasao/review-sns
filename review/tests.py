from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from .views import HomeView

class ReviewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_review_home_review(self):
        request = self.factory.get(reverse('home'))
        request.user = AnonymousUser()

        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed(template_name='review/home.html'):
            response.render()