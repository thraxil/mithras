from django.test import TestCase
from .factories import UsersFactory, PostFactory
from ..models import class_from_weight


class UsersTest(TestCase):
    def test_str(self):
        u = UsersFactory()
        self.assertTrue(u.username in str(u))


class PostTest(TestCase):
    def test_str(self):
        p = PostFactory()
        self.assertEqual(str(p), p.node.title)


class ClassFromWeightTest(TestCase):
    def test_zero(self):
        thresholds = [1.0, 2.9925557394776896, 8.955389853880861,
                      26.799503306491435, 80.19900743499228]
        self.assertEqual(class_from_weight(0, thresholds), 1.0)
