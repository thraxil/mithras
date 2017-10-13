from django.test import TestCase
from .factories import (
    UsersFactory, PostFactory, TagFactory, BookmarkFactory, ImageFactory,
    NodeFactory,
)
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


class ImageTest(TestCase):
    def test_str(self):
        i = ImageFactory()
        self.assertTrue(i.node.title in str(i))

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


class TestNode(TestCase):
    def test_p(self):
        p = PostFactory()
        self.assertEqual(p, p.node.p())

    def test_b(self):
        b = BookmarkFactory()
        self.assertEqual(b, b.node.b())

    def test_i(self):
        i = ImageFactory()
        self.assertEqual(i, i.node.i())

    def test_is_post(self):
        p = NodeFactory(type='post')
        b = NodeFactory(type='bookmark')
        i = NodeFactory(type='image')

        self.assertTrue(p.is_post())
        self.assertFalse(b.is_post())
        self.assertFalse(i.is_post())

    def test_is_bookmark(self):
        p = NodeFactory(type='post')
        b = NodeFactory(type='bookmark')
        i = NodeFactory(type='image')

        self.assertFalse(p.is_bookmark())
        self.assertTrue(b.is_bookmark())
        self.assertFalse(i.is_bookmark())

    def test_is_image(self):
        p = NodeFactory(type='post')
        b = NodeFactory(type='bookmark')
        i = NodeFactory(type='image')

        self.assertFalse(p.is_image())
        self.assertFalse(b.is_image())
        self.assertTrue(i.is_image())

    def test_has_comments(self):
        n = NodeFactory()
        self.assertFalse(n.has_comments())

    def test_num_comments(self):
        n = NodeFactory()
        self.assertEqual(n.num_comments(), 0)

    def test_top_level_comments(self):
        n = NodeFactory()
        self.assertEqual(n.top_level_comments().count(), 0)

    def test_has_tags(self):
        n = NodeFactory()
        self.assertFalse(n.has_tags())

    def test_tags_string(self):
        n = NodeFactory()
        self.assertFalse(n.tags_string(), "")

    def test_add_tag(self):
        n = NodeFactory()
        n.add_tag("foo")
        self.assertEqual(n.get_tags().count(), 1)

    def test_add_tag_from_string(self):
        n = NodeFactory()
        n.add_tag_from_string("foo")
        self.assertEqual(n.get_tags().count(), 1)

    def test_post_count(self):
        n = NodeFactory()
        self.assertEqual(n.post_count(), 0)
        p = PostFactory()
        self.assertEqual(p.node.post_count(), 1)
