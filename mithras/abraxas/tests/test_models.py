from django.test import TestCase
from .factories import (
    UsersFactory, PostFactory, TagFactory, BookmarkFactory, ImageFactory)
from ..models import (
    class_from_weight, make_slug, get_or_create_tag,
    Tag,
)


class UsersTest(TestCase):
    def test_str(self):
        u = UsersFactory()
        self.assertTrue(u.username in str(u))


class PostTest(TestCase):
    def test_str(self):
        p = PostFactory()
        self.assertEqual(str(p), p.node.title)

    def test_update_post(self):
        p = PostFactory()
        p.node.update_post("new title", "new body", p.user, "tags")
        np = p.node.p()
        self.assertEqual(p.node.title, "new title")
        self.assertEqual(np.body, "new body")


class BookmarkTest(TestCase):
    def test_str(self):
        b = BookmarkFactory()
        self.assertEqual(str(b), b.node.title)

    def test_textile(self):
        b = BookmarkFactory()
        self.assertFalse(b.textile())
        b.format = 'textile'
        b.save()
        self.assertTrue(b.textile())


class ImageTest(TestCase):
    def test_str(self):
        i = ImageFactory()
        self.assertTrue(i.node.title in str(i))

    def test_textile(self):
        i = ImageFactory()
        self.assertFalse(i.textile())
        i.format = 'textile'
        i.save()
        self.assertTrue(i.textile())

    def test_scaled_image_url(self):
        i = ImageFactory()
        self.assertTrue(i.rhash in i.scaled_image_url())
        i.rhash = ""
        i.save()
        self.assertTrue("pomelo" in i.scaled_image_url())


class ClassFromWeightTest(TestCase):
    def test_zero(self):
        thresholds = [1.0, 2.9925557394776896, 8.955389853880861,
                      26.799503306491435, 80.19900743499228]
        self.assertEqual(class_from_weight(0, thresholds), 1.0)


class TagTest(TestCase):
    def test_get_absolute_url(self):
        t = TagFactory(slug="example")
        self.assertEqual(t.get_absolute_url(), "/tags/example/")

    def test_unicode(self):
        t = TagFactory(name="example")
        self.assertEqual(str(t), 'example')

    def test_clear_if_empty(self):
        t = TagFactory()
        t.clear_if_empty()


class MakeSlugTest(TestCase):
    def test_empty(self):
        self.assertEqual(make_slug(""), "-")

    def test_not_empty(self):
        self.assertEqual(make_slug(" foo  "), "foo")


class TestGetOrCreateTag(TestCase):
    def test_none(self):
        get_or_create_tag('foo')
        self.assertEqual(Tag.objects.count(), 1)

    def test_existing(self):
        get_or_create_tag('foo')
        get_or_create_tag('foo')
        self.assertEqual(Tag.objects.count(), 1)
