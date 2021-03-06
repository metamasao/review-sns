from django.test import TestCase
from accounts.models import CustomUser, Follow, Action

class CustomUserTest(TestCase):
    """
    accounts.modelsのテスト
    """
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
        """
        CustomUserの属性が適切に保存されているかのテスト
        """
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.email, 'testuser1@email.com')
        self.assertURLEqual(self.user1.get_absolute_url(), f'/review/{self.user1.pk}/author-detail/')
        self.assertEqual(self.user1.url_name, 'review:author-detail')

    def test_follow(self):
        """
        適切にフォローできているかのテスト
        """
        follow_representaion = f'{self.user1.username} follows {self.user2.username}'
        
        self.assertIn(self.user1, self.user2.followers.all())
        self.assertNotIn(self.user2, self.user1.followers.all())
        self.assertEqual(self.follow.__str__(), follow_representaion)

    def test_action(self):
        """
        フォローした時のユーザーのアクションが適切に保存されているかのテスト
        """
        action_content = f'{self.user1.username}さんが{self.user2.username}さんをフォローしました。'
        get_action_content = Action.objects.get_action_content(self.user1, self.user2)

        self.assertEqual(get_action_content, action_content)
        self.assertEqual(self.user1.accounts_actions.all()[0].action_content, action_content)
        self.assertEqual(self.user2.accounts_actions.all().count(), 0)
        self.assertURLEqual(self.user1.accounts_actions.all()[0].action_url, self.user2.get_absolute_url())
        self.assertEqual(self.user1.accounts_actions.all()[0].__str__(), action_content)
        
