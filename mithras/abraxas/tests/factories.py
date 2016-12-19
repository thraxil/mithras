import factory
from mithras.abraxas.models import (
    Users, Node, Post, Tag, Bookmark
)


class UsersFactory(factory.DjangoModelFactory):
    class Meta:
        model = Users

    username = factory.Sequence(lambda n: "testuser%d" % n)
    email = 'test@example.com'
    fullname = 'test user'
    password = 'foo'
    bio = 'a bio'
    css = ''


class NodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Node

    slug = 'foo'
    status = 'Publish'
    title = 'Foo'
    user = factory.SubFactory(UsersFactory)
    type = 'post'


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    node = factory.SubFactory(NodeFactory)
    body = 'some text for the post'
    version = 1
    user = factory.SubFactory(UsersFactory)
    format = 'markdown'


class BookmarkFactory(factory.DjangoModelFactory):
    class Meta:
        model = Bookmark

    node = factory.SubFactory(NodeFactory)
    description = 'some text for the post'
    version = 1
    user = factory.SubFactory(UsersFactory)
    format = 'markdown'
    url = 'https://example.com/'
    via_name = 'somewhere'
    via_url = 'https://somewhere.example.com/'


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    name = 'example'
    slug = 'example'
