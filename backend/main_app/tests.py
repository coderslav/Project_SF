from django.contrib.auth import get_user_model
from .models import Video, Comment, Like
from django.test import TestCase
from django.core.files import File

class UsersManagersTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User = get_user_model()

        cls.user = User.objects.create(
            username = 'test_nickname',
            last_login = '2022-05-15 19:17:42.883254+00:00',
            date_joined = '2022-05-10 21:17:42.883254+00:00',
        )

        cls.superuser = User.objects.create_superuser(
            username = 'test_admin',
            last_login = '2022-05-09 17:17:42.883254+00:00',
            date_joined = '2022-05-08 14:17:42.883254+00:00',
        )

        cls.video = Video.objects.create(
            title = 'Test video',
            # TODO content = open('media/testfiles/test_video.mp4'),
            user = cls.user
        )
        cls.video.subscribers.set([cls.user, cls.superuser])

        COMMENTS = [{'user': cls.user, 'video': cls.video, 'text': 'Testing 1'}, {'user': cls.superuser, 'video': cls.video, 'text': 'Testing 2'}, {'user': cls.user, 'video': cls.video, 'text': 'Testing 3'}]
        LIKES = [{'user': cls.user, 'video': cls.video}, {'user': cls.superuser, 'video': cls.video}, {'user': cls.user, 'video': cls.video}, {'user': cls.superuser, 'video': cls.video}]

        for comment in COMMENTS:
            Comment.objects.create(user = comment['user'], video = comment['video'], text = comment['text'])

        for like in LIKES:
            Like.objects.create(user = like['user'], video = like['video'])

    def test_user(self):
        self.assertEqual(self.user.username, 'test_nickname')
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_banned)
        self.assertIn('15 19:17:42', self.user.last_login)
        self.assertIn('10 21:17:42', self.user.date_joined)

    def test_superuser(self):
        self.assertEqual(self.superuser.username, 'test_admin')
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
        self.assertFalse(self.superuser.is_banned)
        self.assertIn('09 17:17:42', self.superuser.last_login)
        self.assertIn('08 14:17:42', self.superuser.date_joined)
    
    def test_video(self):
        self.assertEqual(str(self.video.title), 'Test video')
        self.assertEqual(str(self.video.user), 'test_nickname')
        # TODO content test
        self.assertEqual(self.video.subscribers.all().count(), 2)
        self.assertTrue(self.video.created_at)
        self.assertTrue(self.video.updated_at)
        self.assertEqual(self.video.get_comments().count(), 3)
        self.assertEqual(self.video.get_likes(), 4)
    
    def test_likes(self):
        self.assertEqual(Like.objects.all().count(), 4)
    
    def test_comments(self):
        self.assertEqual(Comment.objects.all().count(), 3)