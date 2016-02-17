from django.test import TestCase
from django.test.client import Client
from .factories import PostFactory


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_empty_root(self):
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_nonempty_root(self):
        p = PostFactory()
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in response.content)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEqual(response.status_code, 200)
