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

    def test_user_index(self):
        p = PostFactory()
        response = self.c.get("/users/" + p.node.user.username + "/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in response.content)

    def test_nonempty_feed(self):
        p = PostFactory()
        response = self.c.get("/feeds/main/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in response.content)

    def test_user_feed(self):
        p = PostFactory()
        response = self.c.get("/users/" + p.node.user.username + "/feed/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in response.content)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEqual(response.status_code, 200)


class CommentsTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_preview(self):
        p = PostFactory()
        n = p.node
        n.comments_allowed = True
        n.save()
        response = self.c.post(
            n.get_absolute_url() + "add_comment/",
            dict(
                url="http://foo.example.com/",
                content="some content",
                email='foo@example.com',
                horse='foo bar',
                name='',
            )
        )
        self.assertEqual(response.status_code, 200)
