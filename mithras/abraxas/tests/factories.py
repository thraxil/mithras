import factory

from mithras.abraxas.models import (Bookmark, Comment, Image, Node, Post, Tag,
                                    Users)


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    username = factory.Sequence(lambda n: "testuser%d" % n)
    email = "test@example.com"
    fullname = "test user"
    bio = "a bio"


class NodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Node

    slug = "foo"
    status = "Publish"
    title = "Foo"
    user = factory.SubFactory(UsersFactory)
    type = "post"


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    node = factory.SubFactory(NodeFactory)
    body = "some text for the post"
    version = 1
    user = factory.SubFactory(UsersFactory)


class BookmarkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bookmark

    node = factory.SubFactory(NodeFactory)
    description = "some text for the post"
    version = 1
    user = factory.SubFactory(UsersFactory)
    url = "https://example.com/"
    via_name = "somewhere"
    via_url = "https://somewhere.example.com/"


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    node = factory.SubFactory(NodeFactory)
    description = "some text for the post"
    version = 1
    user = factory.SubFactory(UsersFactory)

    thumb_width = 100
    thumb_height = 100
    height = 1024
    width = 1024
    ext = ".jpg"
    rhash = "wert1234523452345"


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = "example"
    slug = "example"


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    node = factory.SubFactory(NodeFactory)
    body = "here is a comment"
    status = "approved"
    reply_to = 0
