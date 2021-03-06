import django.contrib.auth.views as auth_views
import django.contrib.sitemaps.views
import mithras.abraxas.views as views

from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from expvar.views import ExpVarView
from mithras.abraxas.feeds import MainFeed, UserFeed
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from mithras.abraxas.models import Node
from two_factor.urls import urlpatterns as tf_urls

admin.autodiscover()

node_info_dict = {
    'queryset': Node.objects.all().order_by("-created"),
    'date_field': 'modified',
}
sitemaps = {
    'nodes': GenericSitemap(node_info_dict, priority=0.6),
}

feeds = dict(main=MainFeed)

urlpatterns = [
    url(r'', include(tf_urls)),
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
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^users/$', views.UsersView.as_view(), name='users-index'),
    url(r'^users/(?P<username>.*)/feed/$', UserFeed(), name="user-feed"),
    url(r'^users/(?P<username>\w+)/$', views.UserIndexView.as_view(),
        name="user-index"),
    url(r'^users/(?P<username>\w+)/(?P<type>\w+)s/$',
        views.UserTypeIndexView.as_view(),
        name='user-type-index'),
    url(r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>[0-9]{4})/$',
        views.UserTypeYearIndexView.as_view(),
        name='user-type-year-index'),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/$'),
        views.UserTypeMonthIndexView.as_view(),
        name='user-type-month-index'),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/$'),
        views.UserTypeDayIndexView.as_view(),
        name='user-type-day-index'),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/$'),
        views.NodeView.as_view(), name='node-detail'),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/add_comment/$'),
        views.add_comment,
        name="add-comment"),
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/$'),
        views.NodeView.as_view(), name='node-comments-detail'),
    # user type year month day slug comments atom
    url((r'^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/'
         r'(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/'
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
    url(r'^tags/$', views.TagsView.as_view(), name='tags-index'),
    url(r'^tags/(?P<slug>[^/]+)/$', views.TagView.as_view()),
    url(r'^fields/$', views.fields, name='fields-index'),
    url(r'^fields/(?P<name>[^/]+)/$', views.field),
    url(r'^fields/(?P<name>[^/]+)/(?P<value>.+)/$', views.field_value),
    url(r'^feeds/(?P<url>.*)/$', MainFeed()),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='admin/login.html')),
    url(r'^admin/', admin.site.urls),
    url('^debug/vars$', ExpVarView.as_view(), name='expvar'),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
