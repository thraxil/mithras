from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.utils.feedgenerator import Atom1Feed

from mithras.abraxas.models import Users, newest_posts


class MainFeed(Feed):
    feed_type = Atom1Feed
    title = "thraxil.org"
    link = "/"
    subtitle = "thraxil"

    description_template = "feeds/main_description.html"

    def items(self):
        return newest_posts()[:10]


class UserFeed(Feed):
    feed_type = Atom1Feed
    subtitle = "thraxil"

    def get_user_obj(self, username):
        if len(username) == 0:
            raise FeedDoesNotExist
        return Users.objects.filter(username=username)

    def get_object(self, request, username):
        u = self.get_user_obj(username)
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
