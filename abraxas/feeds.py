from mithras.abraxas.models import Users, newest_posts
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.views import FeedDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404


class MainFeed(Feed):
    feed_type = Atom1Feed
    title = "thraxil.org"
    link = "/"
    subtitle = "thraxil"

    def items(self):
        return newest_posts()[:10]


class UserFeed(Feed):
    feed_type = Atom1Feed
    subtitle = "thraxil"

    def get_object(self, request, username):
        if len(username) == 0:
            raise FeedDoesNotExist
        u = User.objects.filter(username=username)
        if u.count() == 0:
            raise FeedDoesNotExist
        return u[0]

    def title(self, obj):
        return "thraxil.org: %s" % obj.fullname

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "/users/%s/feeds/" % obj.username

    def description(self, obj):
        return "Feed for %s" % obj.fullname

    def items(self, obj):
        return obj.newest_posts()[:10]

