from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from ..models import Comment
from .factories import CommentFactory, PostFactory


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_empty_root(self):
        response = self.c.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_nonempty_root(self):
        p = PostFactory()
        response = self.c.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_index_pagenotinteger(self):
        p = PostFactory()
        response = self.c.get(reverse("index") + "?page=foo")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_index_emptypage(self):
        p = PostFactory()
        response = self.c.get(reverse("index") + "?page=10")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_post_view(self):
        p = PostFactory()
        response = self.c.get(p.node.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_post_view_404(self):
        response = self.c.get(
            reverse(
                "node-detail",
                args=["username", "post", "2017", "01", "01", "not-here"],
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_comment_detail(self):
        c = CommentFactory()
        response = self.c.get(c.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_user_index(self):
        p = PostFactory()
        response = self.c.get(
            reverse("user-index", args=[p.node.user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_user_index_noninteger(self):
        p = PostFactory()
        response = self.c.get(
            reverse("user-index", args=[p.node.user.username]) + "?page=foo"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_user_type_index(self):
        p = PostFactory()
        response = self.c.get(
            reverse("user-type-index", args=[p.node.user.username, "post"])
        )
        self.assertEqual(response.status_code, 200)

    def test_user_year_type_index(self):
        p = PostFactory()
        response = self.c.get(
            reverse(
                "user-type-year-index",
                args=[p.node.user.username, "post", p.node.created.year],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_user_type_year_index(self):
        p = PostFactory()
        response = self.c.get(
            reverse(
                "user-type-year-index",
                args=[p.node.user.username, "post", p.node.created.year],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_user_type_month_index(self):
        p = PostFactory()
        response = self.c.get(
            reverse(
                "user-type-month-index",
                args=[
                    p.node.user.username,
                    "post",
                    p.node.created.year,
                    p.node.created.month,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_user_type_day_index(self):
        p = PostFactory()
        response = self.c.get(
            reverse(
                "user-type-day-index",
                args=[
                    p.node.user.username,
                    "post",
                    p.node.created.year,
                    p.node.created.month,
                    p.node.created.day,
                ],
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_nonempty_feed(self):
        p = PostFactory()
        response = self.c.get("/feeds/main/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_user_feed(self):
        p = PostFactory()
        response = self.c.get(
            reverse("user-feed", args=[p.node.user.username])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(p.node.title in str(response.content))

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEqual(response.status_code, 200)

    def test_expvar(self):
        response = self.c.get(reverse("expvar"))
        self.assertEqual(response.status_code, 200)

    def test_sitemap(self):
        response = self.c.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)

    def test_empty_tags_index(self):
        response = self.c.get(reverse("tags-index"))
        self.assertEqual(response.status_code, 200)

    def test_search_empty(self):
        response = self.c.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.c.get(reverse("search") + "?q=foo")
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
                email="foo@example.com",
                horse="foo bar",
                name="",
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_preview_invalid_reply_to(self):
        p = PostFactory()
        n = p.node
        n.comments_allowed = True
        n.save()
        response = self.c.post(
            n.get_absolute_url() + "add_comment/",
            dict(
                url="http://foo.example.com/",
                content="some content",
                email="foo@example.com",
                horse="foo bar",
                name="",
                reply_to="not a number",
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_submit(self):
        p = PostFactory()
        n = p.node
        n.comments_allowed = True
        n.save()
        response = self.c.post(
            n.get_absolute_url() + "add_comment/",
            dict(
                url="http://foo.example.com/",
                content="some content",
                email="foo@example.com",
                horse="foo bar",
                name="",
                submit="submit comment",
                original_referer=n.get_absolute_url() + "add_comment/",
            ),
            HTTP_REFERER=n.get_absolute_url() + "add_comment/",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), 1)

    def test_submit_honeypot(self):
        p = PostFactory()
        n = p.node
        n.comments_allowed = True
        n.save()
        response = self.c.post(
            n.get_absolute_url() + "add_comment/",
            dict(
                url="http://foo.example.com/",
                content="some content",
                email="foo@example.com",
                horse="foo bar",
                name="stupid spammer",
                submit="submit comment",
                original_referer=n.get_absolute_url() + "add_comment/",
            ),
            HTTP_REFERER=n.get_absolute_url() + "add_comment/",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), 0)
