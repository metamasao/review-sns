import logging
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware


from accounts.views import SignupView, UserFollowView, UserUpdateView

logger = logging.getLogger(__name__)

def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


class AccountsViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='testuser1',
            email='testuser1@email.com',
            password='testpass123'
        )
        self.follow_user = get_user_model().objects.create_user(
            username='followuser',
            email='followuser@email.com',
            password='followuser123'
        )

    def test_signup_view_post(self):
        """
        /accounts/signup/
        リクエストメソッドがPostの場合に、SignUpViewで
        アカウントの登録ができてるかのテスト
        """
        request = self.factory.post(
            '/accounts/signup/', 
            data={
                'username':'testuser2', 
                'email':'testuser2@email.com', 
                'password1':'testpass123',
                'password2':'testpass123'
            }
        )
        request.user = AnonymousUser()
        add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        response = SignupView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_signup_view_get(self):
        """
        /accounts/signup/
        リクエストメソッドがGETの時のSignupViewのテスト
        """
        request = self.factory.get('/accounts/signup/')
        response = SignupView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('CustomUserCreationForm', response.context_data['form'].__class__.__name__)
        with self.assertTemplateUsed('registration/signup.html'):
            response.render()
        with self.assertTemplateNotUsed('accounts/signup.html'):
            response.render()

    def test_user_update_view(self):
        request = self.factory.get(f'/accounts/{self.user.pk}/update/')
        request.user = self.user
        response = UserUpdateView.as_view()(request, pk=self.user.pk)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)
        with self.assertTemplateUsed('accounts/user_update.html'):
            response.render()
        with self.assertTemplateNotUsed('accounts/user_not_update.html'):
            response.render()
        
    def test_user_follow_view_get_bad_request(self):
        request = self.factory.get('/accounts/follow')
        request.user = self.user
        response = UserFollowView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_follow_view_post_bad_request(self):
        request = self.factory.post('/accounts/follow/', data={'id':self.follow_user.pk, 'action':'follow'})
        request.user = self.user
        response = UserFollowView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_follow_view_post_without_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.login(username='testuser1', password='testpass123')
        response = client.post(
            '/accounts/follow/',
            data={
                'id':self.follow_user.pk, 
                'action':'follow'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)
        
    def test_user_follow_view_follow(self):
        request = self.factory.post(
            '/accounts/follow/',
            data={
                'id':self.follow_user.pk,
                'action':'follow'
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        request.user = self.user
        response = UserFollowView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.follow_user.followers.all().count(), 1)

    def test_user_follow_view_unfollow(self):
        request = self.factory.post(
            '/accounts/follow/',
            data={
                'id':self.follow_user.pk,
                'action':'unfollow',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        request.user = self.user
        response = UserFollowView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.follow_user.followers.all().count(), 0)
        
