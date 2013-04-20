from django.conf.urls.defaults import patterns, include, url
from mithras.abraxas.feeds import MainFeed, UserFeed

from django.contrib import admin

admin.autodiscover()

feeds = dict(main=MainFeed)

urlpatterns = patterns(
    '',
    (r'^$', 'mithras.abraxas.views.index'),
    (r'^manage/$', 'mithras.abraxas.views.manage'),
    (r'^add_post/$', 'mithras.abraxas.views.add_post'),
    (r'^browse_posts/$', 'mithras.abraxas.views.browse_posts'),
    (r'^pending_comments/$', 'mithras.abraxas.views.pending_comments'),
    (r'^pending_comments/delete/$',
     'mithras.abraxas.views.delete_pending_comments'),
    (r'^edit_post/(?P<node_id>\d+)/$', 'mithras.abraxas.views.edit_post'),
    (r'^search/$', 'mithras.abraxas.views.search'),
    (r'^users/$', 'mithras.abraxas.views.users'),
    (r'^users/(?P<username>.*)/feed/$', UserFeed()),
    (r'^users/(?P<username>\w+)/$', 'mithras.abraxas.views.user_index'),
    (r'^users/(?P<username>\w+)/(?P<type>\w+)s/$',
     'mithras.abraxas.views.user_type_index'),
    (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/$',
     'mithras.abraxas.views.user_type_year_index'),
    (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/$',
     'mithras.abraxas.views.user_type_month_index'),
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/$'),
     'mithras.abraxas.views.user_type_day_index'),
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/$'),
     'mithras.abraxas.views.node'),
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/add_comment/$'),
     'mithras.abraxas.views.add_comment'),
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/$'),
     'mithras.abraxas.views.node'),
    # user type year month day slug comments atom
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/',
      r'(?P<cyear>\d+)-(?P<cmonth>\d+)-(?P<cday>\d+)-(?P<chour>\d+)'
      r'-(?P<cminute>\d+)-(?P<csecond>\d+)/$'),
     'mithras.abraxas.views.comment'),
    # user type year month day slug version
    # user tags
    # user tag
    # user field
    # user field value
    # user feeds/index.rss
    # user feeds/atom.xml
    (r'^tags/$', 'mithras.abraxas.views.tags'),
    (r'^tags/(?P<tag>[^/]+)/$', 'mithras.abraxas.views.tag'),
    (r'^fields/$', 'mithras.abraxas.views.fields'),
    (r'^fields/(?P<name>[^/]+)/$', 'mithras.abraxas.views.field'),
    (r'^fields/(?P<name>[^/]+)/(?P<value>.+)/$',
     'mithras.abraxas.views.field_value'),
    (r'^feeds/(?P<url>.*)/$', MainFeed()),
    url(r'^logout/$',
        view='django.contrib.auth.logout',
        name='logout'),
    (r'^login/$',
     'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': '/home/anders/code/python/mithras/media/'}),
)
