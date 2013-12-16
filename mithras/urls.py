from django.conf.urls.defaults import patterns, include, url
from mithras.abraxas.feeds import MainFeed, UserFeed
import mithras.abraxas.views as views

from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap

admin.autodiscover()

from mithras.abraxas.models import Node

node_info_dict = {
    'queryset': Node.objects.all(),
    'date_field': 'modified',
}
sitemaps = {
    'nodes': GenericSitemap(node_info_dict, priority=0.6),
}

feeds = dict(main=MainFeed)

urlpatterns = patterns(
    '',
    (r'^$', views.IndexView.as_view()),
    (r'^sitemap\.xml$',
     'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps}),
    (r'^manage/$', views.ManageView.as_view()),
    (r'^add_post/$', views.AddPostView.as_view()),
    (r'^browse_posts/$', views.BrowsePostsView.as_view()),
    (r'^pending_comments/$', views.PendingCommentsView.as_view()),
    (r'^pending_comments/delete/$', views.DeletePendingCommentsView.as_view()),
    (r'^edit_post/(?P<node_id>\d+)/$', views.EditPostView.as_view()),
    (r'^search/$', 'mithras.abraxas.views.search'),
    (r'^users/$', views.UsersView.as_view()),
    (r'^users/(?P<username>.*)/feed/$', UserFeed()),
    (r'^users/(?P<username>\w+)/$', views.UserIndexView.as_view()),
    (r'^users/(?P<username>\w+)/(?P<type>\w+)s/$',
     views.UserTypeIndexView.as_view()),
    (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/$',
     views.UserTypeYearIndexView.as_view()),
    (r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/(?P<month>\d+)/$',
     views.UserTypeMonthIndexView.as_view()),
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/$'),
     views.UserTypeDayIndexView.as_view()),
    ((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
      r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/$'),
     views.NodeView.as_view()),
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
     views.CommentView.as_view()),
    # user type year month day slug version
    # user tags
    # user tag
    # user field
    # user field value
    # user feeds/index.rss
    # user feeds/atom.xml
    (r'^tags/$', views.TagsView.as_view()),
    (r'^tags/(?P<tag>[^/]+)/$', views.TagView.as_view()),
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
)
