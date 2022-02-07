from django.test import TestCase, RequestFactory
from django.urls import reverse

from .models import CustomUser, Follow, Event
from .views import SingupView

class CustomUserTest(TestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )

        self.user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@email.com',
            password='testpass234'
        )

        self.follow = Follow.objects.create_follow(self.user1, self.user2)

    def test_custom_user_attribute(self):
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.email, 'testuser1@email.com')
        self.assertEqual(self.user1.get_absolute_url(), f'/accounts/{self.user1.username}/{self.user1.pk}/')

    def test_follow(self):
        follow_representaion = f'{self.user1.username} follows {self.user2.username}'
        
        self.assertIn(self.user1, self.user2.followers.all())
        self.assertNotIn(self.user2, self.user1.followers.all())
        self.assertEqual(str(self.follow), follow_representaion)

    def test_event(self):
        event_content = f'{self.user1.username}さんが{self.user2.username}さんをフォローしました。'
        get_event_content = Event.objects.get_event_content(self.user1, self.user2)
        self.assertEqual(get_event_content, event_content)
        self.assertEqual(self.user1.events.all()[0].event, event_content)
        self.assertEqual(self.user2.events.all().count(), 0)
        self.assertEqual(self.user1.events.all()[0].event_url, self.user2.get_absolute_url())
        
        
class ReviewViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )

    def test_signup(self):
        request = self.factory.get(reverse('home'))
        request.user = self.user
        response = SingupView.as_view()(request)

        self.assertEqual(response.status_code, 200)