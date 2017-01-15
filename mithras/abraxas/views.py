from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import django
from django.core.cache import cache
from django.core.mail import mail_managers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.dates import DayArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from models import Node, Post, Bookmark, Image, Users, Comment, MetaField, Tag
from models import newest_posts, all_pending_comments, make_slug, scaled_tags


def uniquify(lst):
    return list(set(lst))


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = "abraxas/index.html"

    def get_context_data(self):
        paginator = Paginator(newest_posts(), 10)
        try:
            p = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            p = paginator.page('1')
        except EmptyPage:
            p = paginator.page('1')
        return dict(posts=p.object_list, paginator=p)


def search(request):
    q = request.GET.get("q", "")
    nodes = []
    if q != "":
        title_matches = list(Node.objects.filter(title__icontains=q))[:50]
        post_matches = [p.node for p
                        in Post.objects.filter(body__icontains=q)][:50]
        bookmark_matches = [
            p.node for p
            in Bookmark.objects.filter(
                description__icontains=q)][:50]
        image_matches = [
            p.node for p
            in Image.objects.filter(
                description__icontains=q)][:50]
        nodes = uniquify(title_matches + post_matches + bookmark_matches +
                         image_matches)
        nodes.sort(key=lambda x: x.created)
        nodes.reverse()
    return render(request, "abraxas/search_results.html",
                  dict(q=q, nodes=nodes))


class BrowsePostsView(LoggedInMixin, TemplateView):
    template_name = "abraxas/browse.html"

    def get_context_data(self):
        paginator = Paginator(newest_posts(), 100)
        try:
            p = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            p = paginator.page('1')
        return dict(posts=p.object_list, paginator=p)


class PendingCommentsView(LoggedInMixin, TemplateView):
    template_name = "abraxas/pending.html"

    def get_context_data(self):
        paginator = Paginator(all_pending_comments(), 100)
        try:
            p = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            p = paginator.page('1')

        return dict(comments=p.object_list, paginator=p)


class DeletePendingCommentsView(LoggedInMixin, View):
    def post(self, request):
        for comment in all_pending_comments():
            comment.delete()
        return HttpResponseRedirect("/pending_comments/")


class DeleteNodeView(LoggedInMixin, DeleteView):
    model = Node
    success_url = "/browse_posts/"


class EditPostView(LoggedInMixin, View):
    template_name = "abraxas/edit_post.html"

    def post(self, request, node_id):
        node = get_object_or_404(Node, id=node_id)
        title = request.POST.get("title", node.title)
        body = request.POST.get("body", "")
        tags = request.POST.get("tags", "")
        user = get_object_or_404(Users, username=request.user.username)
        node.update_post(title, body, user, tags)
        cache.clear()
        return HttpResponseRedirect("/edit_post/%d/" % node.id)

    def get(self, request, node_id):
        node = get_object_or_404(Node, id=node_id)
        return render(request, self.template_name, dict(node=node))


class ManageView(LoggedInMixin, TemplateView):
    template_name = "abraxas/manage.html"


class AddPostView(LoggedInMixin, View):
    template_name = "abraxas/add_post.html"

    def get_node(self, request, title, user):
        if request.POST.get("node_id", "") == "":
            return Node.objects.create(title=title, slug=make_slug(title),
                                       type="post", comments_allowed=True,
                                       user=user, status="Draft")
        else:
            return get_object_or_404(Node, id=request.POST["node_id"])

    def post(self, request):
        title = request.POST.get("title", "no title")
        body = request.POST.get("body", "")
        tags = request.POST.get("tags", "")
        user = get_object_or_404(Users, username=request.user.username)
        node = self.get_node(request, title, user)

        if request.POST.get("preview", "") == "Preview":
            return render(request, self.template_name,
                          dict(preview=True, node_id=node.id,
                               title=title, body=body, tags=tags))
        else:
            node.set_tags(tags)
            node.title = title
            node.slug = make_slug(title)
            Post.objects.create(node=node, body=body,
                                version=node.post_count() + 1, user=user,
                                format="markdown")
            node.status = "Publish"
            node.save()
            cache.clear()
            return HttpResponseRedirect(node.get_absolute_url())

    def get(self, request):
        return render(request, self.template_name,
                      dict(preview=False, node_id=""))


class UsersView(ListView):
    model = Users
    template_name = "abraxas/users.html"
    context_object_name = "users"


class UserIndexView(TemplateView):
    template_name = "abraxas/user_index.html"

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        user = get_object_or_404(Users, username=username)
        paginator = Paginator(user.newest_posts(), 10)
        try:
            p = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            p = paginator.page('1')
        return dict(user=user, posts=p.object_list, paginator=p)


class UserTypeIndexView(TemplateView):
    template_name = "abraxas/user_type_index.html"

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        t = kwargs['type']
        user = get_object_or_404(Users, username=username)
        nodes = Node.objects.filter(user=user, type=t, status="Publish")
        years = uniquify([n.created.year for n in nodes])
        return dict(user=user, type=t, years=years)


class UserTypeYearIndexView(TemplateView):
    template_name = "abraxas/user_type_year_index.html"

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        t = kwargs['type']
        year = kwargs['year']
        user = get_object_or_404(Users, username=username)
        nodes = Node.objects.filter(
            user=user, type=t, status="Publish",
            created__startswith="%04d" % int(year))
        months = uniquify([n.created.month for n in nodes])
        return dict(user=user, type=t, year=year, months=months)


class UserTypeMonthIndexView(TemplateView):
    template_name = "abraxas/user_type_month_index.html"

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        t = kwargs['type']
        year = kwargs['year']
        month = kwargs['month']
        user = get_object_or_404(Users, username=username)
        nodes = Node.objects.filter(
            user=user, type=t, status="Publish",
            created__startswith="%04d-%02d" % (int(year), int(month)))
        days = uniquify([n.created.day for n in nodes])
        return dict(user=user, type=t, year=year,
                    month=month, days=days)


class UserTypeDayIndexView(DayArchiveView):
    template_name = "abraxas/user_type_day_index.html"
    date_field = "created"
    model = Node
    month_format = '%m'
    context_object_name = 'nodes'

    def get_queryset(self):
        return Node.objects.filter(
            user__username=self.kwargs['username'],
            type=self.kwargs['type'], status="Publish")

    def get_context_data(self, **kwargs):
        context = super(UserTypeDayIndexView, self).get_context_data(**kwargs)
        context['user'] = get_object_or_404(
            Users, username=self.kwargs['username'])
        context['type'] = self.kwargs['type']
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['day'] = self.kwargs['day']
        return context


def get_node_or_404(**kwargs):
    try:
        return get_object_or_404(Node, **kwargs)
    except django.core.exceptions.MultipleObjectsReturned:
        r = Node.objects.filter(
            user=kwargs['user'], type=kwargs['type'],
            created__startswith=kwargs['created__startswith'],
            slug=kwargs['slug'])
        return r[0]


class NodeView(TemplateView):
    template_name = "abraxas/node.html"

    def get_context_data(self, username, type, year, month, day, slug):
        user = get_object_or_404(Users, username=username)
        node = get_node_or_404(
            user=user, type=type, status="Publish",
            created__startswith="%04d-%02d-%02d" % (int(year),
                                                    int(month), int(day)),
            slug=slug)
        return dict(node=node)


class CommentView(TemplateView):
    template_name = "abraxas/comment.html"

    def get_context_data(self, username, type, year, month, day, slug, cyear,
                         cmonth, cday, chour, cminute, csecond):
        user = get_object_or_404(Users, username=username)
        node = get_node_or_404(
            user=user, type=type, status="Publish",
            created__startswith="%04d-%02d-%02d" % (
                int(year), int(month), int(day)),
            slug=slug)
        comment = get_object_or_404(
            Comment, node=node,
            created__startswith="%04d-%02d-%02d %02d:%02d:%02d" % (
                int(cyear), int(cmonth), int(cday),
                int(chour), int(cminute), int(csecond)),
        )
        return dict(node=node, comment=comment)


def block_non_integer_and_honeypot(request):
    # some spammers submit reply_to with non-integers for some reason
    # so if we see that we can reject it immediately
    referer = request.META.get('HTTP_REFERER', "/")
    try:
        int(request.POST.get('reply_to', '0'))
    except ValueError:
        # let them think they succeeded
        return HttpResponse(
            "your comment has been submitted and is pending moderator "
            "approval. <a href='%s'>return</a>" % referer)
    # "name" is a honeypot field. spammers fill it out
    # but browsers don't display it. if it has a value,
    # we know it wasn't a real person
    if request.POST.get('name', '') != "":
        # again, let them think they got through
        return HttpResponse(
            "your comment has been submitted and is pending moderator "
            "approval. <a href='%s'>return</a>" % referer)
    return None


def clean_url(url):
    if url == "":
        return ""
    return clean_url_not_empty(url)


def clean_url_not_empty(url):
    if not url.startswith("http://"):
        url = "http://" + url
    return url


def check_referer_for_spammer(request, referer):
    # if referer doesn't end in "add_comment/",
    # we know they didn't preview and are thus spam
    if not referer.endswith("add_comment/"):
        return HttpResponse("go away, spammer")
    return check_referer_for_spammer_good_path(request, referer)


def check_referer_for_spammer_good_path(request, referer):
    referer = request.POST.get('original_referer', '')
    if referer == '':
        return HttpResponse("go away, spammer")
    return None


def handle_empty_required_fields(request):
    # "horse" is the random replacement name for what
    # would otherwise be "name"
    if (request.POST.get('horse', '') == "" or
            request.POST.get('email', '') == ""):
        return HttpResponse("name and email are required fields")
    return handle_empty_required_fields_has_name_email(request)


def handle_empty_required_fields_has_name_email(request):
    if request.POST.get('content', '') == "":
        return HttpResponse("no content in your comment")
    return None


def add_comment_not_honeypot(request, username, type, year, month, day, slug):
    user = get_object_or_404(Users, username=username)
    node = get_node_or_404(
        user=user, type=type, status="Publish",
        created__startswith="%04d-%02d-%02d" % (
            int(year), int(month), int(day)),
        slug=slug)
    if not node.comments_allowed:
        return HttpResponse("sorry, no comments allowed on this one")
    return add_comment_comments_allowed(request, node, user)


def add_comment_comments_allowed(request, node, user):
    url = clean_url(request.POST.get("url", ""))
    r = handle_empty_required_fields(request)
    if r is not None:
        return r
    return add_comment_has_required_fields(request, node, user, url)


def preview_comment(request, referer, node, url):
    referer = request.POST.get('original_referer', referer)
    return render(
        request, "abraxas/preview.html",
        dict(node=node, name=request.POST['name'],
             url=url,
             original_referer=referer,
             email=request.POST['email'],
             content=request.POST['content'],
             reply_to=int(request.POST.get('reply_to', '0'))))


def add_comment_has_required_fields(request, node, user, url):
    referer = request.META.get('HTTP_REFERER', node.get_absolute_url())
    if request.POST.get('submit', '') != "submit comment":
        return preview_comment(request, referer, node, url)
    return add_comment_not_preview(request, referer, node, url)


def add_comment_not_preview(request, referer, node, url):
    r = check_referer_for_spammer(request, referer)
    if r is not None:
        return r
    return add_comment_for_real(request, url, node, referer)


def add_comment_for_real(request, url, node, referer):
    c = Comment(author_name=request.POST['name'],
                author_url=url,
                author_email=request.POST['email'],
                body=request.POST['content'],
                node=node,
                status=determine_comment_status(request),
                reply_to=int(request.POST.get('reply_to', '0')))
    c.save()
    cache.clear()
    return add_comment_final_response(c, node, referer)


def add_comment_final_response(c, node, referer):
    if c.status == "pending":
        subject = "new comment on %s" % node.title
        message = comment_email_body(c)
        mail_managers(subject, message, fail_silently=False)
        return HttpResponse(
            "your comment has been submitted and is pending moderator "
            "approval. <a href='%s'>return</a>" % referer)
    return HttpResponseRedirect(referer)


def add_comment(request, username, type, year, month, day, slug):
    r = block_non_integer_and_honeypot(request)
    if r is not None:
        return r
    return add_comment_not_honeypot(request, username, type,
                                    year, month, day, slug)


def determine_comment_status(request):
    if not request.user.is_anonymous():
        return "approved"
    return "pending"


def comment_email_body(c):
    return """comment from: %s

------
%s
------

to approve or delete, go here:
http://thraxil.org/admin/abraxas/comment/%d/
            """ % (c.author_name, c.body, c.id)


def ufield(f, ufields, seen):
    if f.field_name not in seen:
        ufields.append(f)
        seen[f.field_name] = 1
    return ufields, seen


def fields(request):
    all_fields = MetaField.objects.all()
    seen = dict()
    ufields = []
    for f in all_fields:
        ufields, seen = ufield(f, ufields, seen)
    return render(request, "abraxas/fields.html", dict(fields=ufields))


def field(request, name):
    all_fields = MetaField.objects.filter(field_name__iexact=name)
    seen = dict()
    ufields = []
    for f in all_fields:
        seen, ufields = handle_field(f, seen, ufields)
    return render(request, "abraxas/field.html",
                  dict(fields=ufields, name=name))


def handle_field(f, seen, ufields):
    if f.field_value not in seen:
        ufields.append(f)
        seen[f.field_value] = 1
    return seen, ufields


def field_value(request, name, value):
    nodes = [
        f.node for f in MetaField.objects.filter(
            field_name__iexact=name,
            field_value__iexact=value)]
    return render(request, "abraxas/field_value.html",
                  dict(nodes=nodes, name=name, value=value))


class TagsView(TemplateView):
    template_name = "abraxas/tags.html"

    def get_context_data(self):
        tags = scaled_tags()
        return dict(tags=tags)


class TagView(DetailView):
    model = Tag
    template_name = "abraxas/tag.html"
    context_object_name = "tag"
