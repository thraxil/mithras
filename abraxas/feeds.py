from mithras.abraxas.models import *
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.syndication import feeds
from django.http import HttpResponse, Http404

class MainFeed(Feed):
    feed_type = Atom1Feed
    title = "thraxil.org"
    link = "/"
    subtitle = "thraxil"

    def items(self):
        return newest_posts()

class UserFeed(Feed):
    feed_type = Atom1Feed
    subtitle = "thraxil"
    def get_object(self,bits):
        if len(bits) != 1:
            raise FeedDoesNotExist
        return get_object_or_404(Users,username=bits[0])

    def title(self,obj):
        return "thraxil.org: %s" % obj.fullname

    def link(self,obj):
        if not obj:
            raise FeedDoesNotExist
        return "/users/%s/feeds/" % obj.username

    def description(self, obj):
        return "Feed for %s" % obj.fullname

    def items(self, obj):
        return obj.newest_posts()

def dispatch_user_feed(request,username):
    try:
        feedgen = UserFeed('main',request).get_feed(username)
    except feeds.FeedDoesNotExist:
        raise Http404, "No such user"
    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response,'utf-8')
    return response


        
    
