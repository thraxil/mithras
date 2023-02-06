import django.contrib.auth.views as auth_views
import django.contrib.sitemaps.views
from django.conf import settings
from django.conf.urls import include, re_path
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from expvar.views import ExpVarView

import mithras.abraxas.views as views
from mithras.abraxas.feeds import MainFeed, UserFeed
from mithras.abraxas.models import Node

admin.autodiscover()

node_info_dict = {
    "queryset": Node.objects.all().order_by("-created"),
    "date_field": "modified",
}
sitemaps = {
    "nodes": GenericSitemap(node_info_dict, priority=0.6),
}

feeds = dict(main=MainFeed)

urlpatterns = [
    re_path(r"^$", views.IndexView.as_view(), name="index"),
    re_path(
        r"^sitemap\.xml$",
        django.contrib.sitemaps.views.sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    re_path(r"smoketest/", include("smoketest.urls")),
    re_path(r"^manage/$", views.ManageView.as_view()),
    re_path(r"^add_post/$", views.AddPostView.as_view()),
    re_path(r"^browse_posts/$", views.BrowsePostsView.as_view()),
    re_path(
        r"^node/(?P<pk>\d+)/delete/$",
        views.DeleteNodeView.as_view(),
        name="delete-node",
    ),
    re_path(r"^pending_comments/$", views.PendingCommentsView.as_view()),
    re_path(
        r"^pending_comments/delete/$",
        views.DeletePendingCommentsView.as_view(),
    ),
    re_path(r"^edit_post/(?P<node_id>\d+)/$", views.EditPostView.as_view()),
    re_path(r"^search/$", views.SearchView.as_view(), name="search"),
    re_path(r"^users/$", views.UsersView.as_view(), name="users-index"),
    re_path(r"^users/(?P<username>.*)/feed/$", UserFeed(), name="user-feed"),
    re_path(
        r"^users/(?P<username>\w+)/$",
        views.UserIndexView.as_view(),
        name="user-index",
    ),
    re_path(
        r"^users/(?P<username>\w+)/(?P<type>\w+)s/$",
        views.UserTypeIndexView.as_view(),
        name="user-type-index",
    ),
    re_path(
        r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>[0-9]{4})/$",
        views.UserTypeYearIndexView.as_view(),
        name="user-type-year-index",
    ),
    re_path(
        (
            r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/"
            r"(?P<month>\d+)/$"
        ),
        views.UserTypeMonthIndexView.as_view(),
        name="user-type-month-index",
    ),
    re_path(
        (
            r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/"
            r"(?P<month>\d+)/(?P<day>\d+)/$"
        ),
        views.UserTypeDayIndexView.as_view(),
        name="user-type-day-index",
    ),
    re_path(
        (
            r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/"
            r"(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/$"
        ),
        views.NodeView.as_view(),
        name="node-detail",
    ),
    re_path(
        (
            r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/"
            r"(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/add_comment/$"
        ),
        views.add_comment,
        name="add-comment",
    ),
    re_path(
        (
            r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/"
            r"(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/$"
        ),
        views.NodeView.as_view(),
        name="node-comments-detail",
    ),
    # user type year month day slug comments atom
    re_path(
        (
            r"^users/(?P<username>\w+)/(?P<type>\w+)s/(?P<year>\d+)/"
            r"(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w\-]+)/comments/"
            r"(?P<cyear>\d+)-(?P<cmonth>\d+)-(?P<cday>\d+)-(?P<chour>\d+)"
            r"-(?P<cminute>\d+)-(?P<csecond>\d+)/$"
        ),
        views.CommentView.as_view(),
    ),
    # user type year month day slug version
    # user tags
    # user tag
    # user field
    # user field value
    # user feeds/index.rss
    # user feeds/atom.xml
    re_path(r"^tags/$", views.TagsView.as_view(), name="tags-index"),
    re_path(r"^tags/(?P<slug>[^/]+)/$", views.TagView.as_view()),
    re_path(r"^fields/$", views.fields, name="fields-index"),
    re_path(r"^fields/(?P<name>[^/]+)/$", views.field),
    re_path(r"^fields/(?P<name>[^/]+)/(?P<value>.+)/$", views.field_value),
    re_path(r"^feeds/(?P<url>.*)/$", MainFeed()),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    re_path(
        r"^login/$",
        auth_views.LoginView.as_view(template_name="admin/login.html"),
    ),
    re_path(r"^admin/", admin.site.urls),
    re_path("^debug/vars$", ExpVarView.as_view(), name="expvar"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
