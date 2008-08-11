from mithras.abraxas.models import *
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

class MainFeed(Feed):
    feed_type = Atom1Feed
    title = "thraxil.org"
    link = "/"
    subtitle = "thraxil"

    def items(self):
        return newest_posts()

