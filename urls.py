from django.conf.urls.defaults import *
from mithras.abraxas.feeds import MainFeed,dispatch_user_feed

from django.contrib import admin

admin.autodiscover()

feeds = dict(main=MainFeed)

urlpatterns = patterns('',
                       (r'^$','abraxas.views.index'),
                       (r'^add_post/$','abraxas.views.add_post'),
                       (r'^search/$','abraxas.views.search'),
                       (r'^users/$','abraxas.views.users'),
                       (r'^users/(?P<username>.*)/feed/$','abraxas.feeds.dispatch_user_feed'),
                       (r'^users/(?P<username>\w+)/$','abraxas.views.user_index'),
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/$','abraxas.views.user_type_index'),
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/$','abraxas.views.user_type_year_index'),
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/$','abraxas.views.user_type_month_index'),                       
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$','abraxas.views.user_type_day_index'),
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/$','abraxas.views.node'),
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/add_comment/$','abraxas.views.add_comment'),
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/$','abraxas.views.node'),
                       # user type year month day slug comments atom
                       (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/(?P<cyear>\d+)-(?P<cmonth>\d+)-(?P<cday>\d+)-(?P<chour>\d+)-(?P<cminute>\d+)-(?P<csecond>\d+)/$','abraxas.views.comment'),
                       # user type year month day slug version
                       # user tags
                       # user tag
                       # user field
                       # user field value
                       # user feeds/index.rss
                       # user feeds/atom.xml
                       (r'^tags/$','abraxas.views.tags'),
                       (r'^tags/(?P<tag>[^/]+)/$','abraxas.views.tag'),
                       (r'^fields/$','abraxas.views.fields'),
                       (r'^fields/(?P<name>[^/]+)/$','abraxas.views.field'),
                       (r'^fields/(?P<name>[^/]+)/(?P<value>.+)/$','abraxas.views.field_value'),                       
                       (r'^feeds/(?P<url>.*)/$','django.contrib.syndication.views.feed',{'feed_dict' : feeds}),
                       (r'^admin/(.*)', admin.site.root),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anders/code/python/mithras/media/'}),
                        
)
