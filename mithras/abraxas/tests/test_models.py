from django.test import TestCase
from .factories import UsersFactory, PostFactory


class UsersTest(TestCase):
    def test_str(self):
        u = UsersFactory()
        self.assertTrue(u.username in str(u))


class PostTest(TestCase):
    def test_str(self):
        p = PostFactory()
        self.assertEqual(str(p), p.node.title)
