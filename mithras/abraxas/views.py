from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import django
from django.core.mail import mail_managers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from models import Node, Post, Bookmark, Image, Users, Comment, MetaField, Tag
from models import newest_posts, all_pending_comments, make_slug, scaled_tags


def uniquify(lst):
    s = dict()
    o = []
    for i in lst:
        if i not in s:
            o.append(i)
            s[i] = 1
    return o


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        paginator = Paginator(newest_posts(), 10)
        try:
            p = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            p = paginator.page('1')
        return dict(posts=p.object_list, paginator=p)


def search(request):
    q = request.GET.get("q", "")
    nodes = []
    if q != "":
        title_matches = list(Node.objects.filter(title__icontains=q))[:50]
        post_matches = [p.node for p
                        in Post.objects.filter(body__icontains=q)][:50]
        bookmark_matches = [p.node for p
                            in Bookmark.objects.filter(
                            description__icontains=q)][:50]
        image_matches = [p.node for p
                         in Image.objects.filter(
                         description__icontains=q)][:50]
        nodes = uniquify(title_matches + post_matches
                         + bookmark_matches + image_matches)
        nodes.sort(key=lambda x: x.created)
        nodes.reverse()
    return render(request, "search_results.html", dict(q=q, nodes=nodes))


class BrowsePostsView(LoggedInMixin, TemplateView):
    template_name = "browse.html"

    def get_context_data(self):
        paginator = Paginator(newest_posts(), 100)
        try:
            p = paginator.page(self.request.GET.get('page', '1'))
        except PageNotAnInteger:
            p = paginator.page('1')
        return dict(posts=p.object_list, paginator=p)


class PendingCommentsView(LoggedInMixin, TemplateView):
    template_name = "pending.html"

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


class EditPostView(LoggedInMixin, View):
    template_name = "edit_post.html"

    def post(self, request, node_id):
        node = get_object_or_404(Node, id=node_id)
        title = request.POST.get("title", node.title)
        body = request.POST.get("body", "")
        tags = request.POST.get("tags", "")
        user = get_object_or_404(Users, username=request.user.username)
        Post.objects.create(node=node, body=body,
                            version=node.post_count() + 1, user=user,
                            format="markdown")
        node.set_tags(tags)
        node.title = title
        node.status = "Publish"
        node.save()
        return HttpResponseRedirect("/edit_post/%d/" % node.id)

    def get(self, request, node_id):
        node = get_object_or_404(Node, id=node_id)
        return render(request, self.template_name, dict(node=node))


class ManageView(LoggedInMixin, TemplateView):
    template_name = "manage.html"


class AddPostView(LoggedInMixin, View):
    template_name = "add_post.html"

    def post(self, request):
        title = request.POST.get("title", "no title")
        body = request.POST.get("body", "")
        tags = request.POST.get("tags", "")
        user = get_object_or_404(Users, username=request.user.username)
        if request.POST.get("node_id", "") == "":
            node = Node.objects.create(title=title, slug=make_slug(title),
                                       type="post", comments_allowed=True,
                                       user=user, status="Draft")
        else:
            node = get_object_or_404(Node, id=request.POST["node_id"])

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
            return HttpResponseRedirect(node.get_absolute_url())

    def get(self, request):
        return render(request, self.template_name,
                      dict(preview=False, node_id=""))


class UsersView(ListView):
    model = Users
    template_name = "users.html"
    context_object_name = "users"


class UserIndexView(TemplateView):
    template_name = "user_index.html"

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
    template_name = "user_type_index.html"

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        t = kwargs['type']
        user = get_object_or_404(Users, username=username)
        nodes = Node.objects.filter(user=user, type=t, status="Publish")
        years = uniquify([n.created.year for n in nodes])
        return dict(user=user, type=t, years=years)


class UserTypeYearIndexView(TemplateView):
    template_name = "user_type_year_index.html"

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
    template_name = "user_type_month_index.html"

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


class UserTypeDayIndexView(TemplateView):
    template_name = "user_type_day_index.html"

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        t = kwargs['type']
        year = kwargs['year']
        month = kwargs['month']
        day = kwargs['day']
        user = get_object_or_404(Users, username=username)
        nodes = Node.objects.filter(
            user=user, type=t, status="Publish",
            created__startswith="%04d-%02d-%02d" % (
                int(year), int(month), int(day)))
        return dict(user=user, type=t, year=year, month=month,
                    day=day, nodes=nodes)


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
    template_name = "node.html"

    def get_context_data(self, username, type, year, month, day, slug):
        user = get_object_or_404(Users, username=username)
        node = get_node_or_404(
            user=user, type=type, status="Publish",
            created__startswith="%04d-%02d-%02d" % (int(year),
                                                    int(month), int(day)),
            slug=slug)
        return dict(node=node)


class CommentView(TemplateView):
    template_name = "comment.html"

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
    if not url == "":
        if not url.startswith("http://"):
            url = "http://" + url
    return url


def check_referer_for_spammer(request, referer):
    # if referer doesn't end in "add_comment/",
    # we know they didn't preview and are thus spam
    if not referer.endswith("add_comment/"):
        return HttpResponse("go away, spammer")
    referer = request.POST.get('original_referer', '')
    if referer == '':
        return HttpResponse("go away, spammer")
    return None


def handle_empty_required_fields(request):
    # "horse" is the random replacement name for what
    # would otherwise be "name"
    if (request.POST.get('horse', '') == ""
            or request.POST.get('email', '') == ""):
        return HttpResponse("name and email are required fields")

    if request.POST.get('content', '') == "":
        return HttpResponse("no content in your comment")
    return None


def add_comment(request, username, type, year, month, day, slug):
    r = block_non_integer_and_honeypot(request)
    if r is not None:
        return r
    user = get_object_or_404(Users, username=username)
    node = get_node_or_404(
        user=user, type=type, status="Publish",
        created__startswith="%04d-%02d-%02d" % (
            int(year), int(month), int(day)),
        slug=slug)
    if not node.comments_allowed:
        return HttpResponse("sorry, no comments allowed on this one")
    url = clean_url(request.POST.get("url", ""))
    r = handle_empty_required_fields(request)
    if r is not None:
        return r

    referer = request.META.get('HTTP_REFERER', node.get_absolute_url())
    if request.POST.get('submit', '') != "submit comment":
        referer = request.POST.get('original_referer', referer)
        return render(
            request, "preview.html",
            dict(node=node, name=request.POST['name'],
                 url=url,
                 original_referer=referer,
                 email=request.POST['email'],
                 content=request.POST['content'],
                 reply_to=int(request.POST.get('reply_to', '0'))))

    r = check_referer_for_spammer(request, referer)
    if r is not None:
        return r

    c = Comment(author_name=request.POST['name'],
                author_url=url,
                author_email=request.POST['email'],
                body=request.POST['content'],
                node=node,
                status=determine_comment_status(request),
                reply_to=int(request.POST.get('reply_to', '0')))
    c.save()
    if c.status == "pending":
        subject = "new comment on %s" % node.title
        message = comment_email_body(c)
        mail_managers(subject, message, fail_silently=False)
        return HttpResponse(
            "your comment has been submitted and is pending moderator "
            "approval. <a href='%s'>return</a>" % referer)
    return HttpResponseRedirect(referer)


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


def fields(request):
    all_fields = MetaField.objects.all()
    seen = dict()
    ufields = []
    for f in all_fields:
        if f.field_name not in seen:
            ufields.append(f)
            seen[f.field_name] = 1
    return render(request, "fields.html", dict(fields=ufields))


def field(request, name):
    all_fields = MetaField.objects.filter(field_name__iexact=name)
    seen = dict()
    ufields = []
    for f in all_fields:
        if f.field_value not in seen:
            ufields.append(f)
            seen[f.field_value] = 1

    return render(request, "field.html", dict(fields=ufields, name=name))


def field_value(request, name, value):
    nodes = [
        f.node for f in MetaField.objects.filter(
            field_name__iexact=name,
            field_value__iexact=value)]
    return render(request, "field_value.html",
                  dict(nodes=nodes, name=name, value=value))


class TagsView(TemplateView):
    template_name = "tags.html"

    def get_context_data(self):
        tags = scaled_tags()
        return dict(tags=tags)


class TagView(DetailView):
    model = Tag
    template_name = "tag.html"
    context_object_name = "tag"
