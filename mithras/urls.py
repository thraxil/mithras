import django.contrib.auth.views
import django.contrib.sitemaps.views
import mithras.abraxas.views as views

from django.conf.urls import include, url
from django.views.generic import TemplateView
from expvar.views import ExpVarView
from mithras.abraxas.feeds import MainFeed, UserFeed
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from mithras.abraxas.models import Node

admin.autodiscover()

node_info_dict = {
    'queryset': Node.objects.all(),
    'date_field': 'modified',
}
sitemaps = {
    'nodes': GenericSitemap(node_info_dict, priority=0.6),
}

feeds = dict(main=MainFeed)

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^sitemap\.xml$',
        django.contrib.sitemaps.views.sitemap,
        {'sitemaps': sitemaps},
        name='sitemap'),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^manage/$', views.ManageView.as_view()),
    url(r'^add_post/$', views.AddPostView.as_view()),
    url(r'^browse_posts/$', views.BrowsePostsView.as_view()),
    url(r'^node/(?P<pk>\d+)/delete/$', views.DeleteNodeView.as_view(),
        name='delete-node'),
    url(r'^pending_comments/$', views.PendingCommentsView.as_view()),
    url(r'^pending_comments/delete/$',
        views.DeletePendingCommentsView.as_view()),
    url(r'^edit_post/(?P<node_id>\d+)/$', views.EditPostView.as_view()),
    url(r'^search/$', views.search, name='search'),
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<username>.*)/feed/$', UserFeed(), name="user-feed"),
    url(r'^users/(?P<username>\w+)/$', views.UserIndexView.as_view(),
        name="user-index"),
    url(r'^users/(?P<username>\w+)/(?P<type>\w+)s/$',
        views.UserTypeIndexView.as_view()),
    url(r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/$',
        views.UserTypeYearIndexView.as_view()),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         '(?P<month>\d+)/$'),
        views.UserTypeMonthIndexView.as_view()),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/$'),
        views.UserTypeDayIndexView.as_view()),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/$'),
        views.NodeView.as_view()),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/add_comment/$'),
        views.add_comment,
        name="add-comment"),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/$'),
        views.NodeView.as_view()),
    # user type year month day slug comments atom
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
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
    url(r'^tags/$', views.TagsView.as_view()),
    url(r'^tags/(?P<slug>[^/]+)/$', views.TagView.as_view()),
    url(r'^fields/$', views.fields),
    url(r'^fields/(?P<name>[^/]+)/$', views.field),
    url(r'^fields/(?P<name>[^/]+)/(?P<value>.+)/$', views.field_value),
    url(r'^feeds/(?P<url>.*)/$', MainFeed()),
    url(r'^logout/$',
        view=django.contrib.auth.logout,
        name='logout'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {'template_name': 'admin/login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url('^debug/vars$', ExpVarView.as_view(), name='expvar'),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
]
