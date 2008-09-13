from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *
import django
from django.core.mail import mail_managers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from mithras.settings import MEDIA_ROOT
import os

def uniquify(lst):
    s = dict()
    o = []
    for i in lst:
        if i not in s:
            o.append(i)
            s[i] = 1
    return o


def index(request):
    paginator = Paginator(newest_posts(), 10)
    p = paginator.page(request.GET.get('page','1'))
    return render_to_response("index.html",dict(posts=p.object_list,paginator=p))

def search(request):
    q = request.GET.get("q","")
    nodes = []
    if q != "":
        title_matches = list(Node.objects.filter(title__icontains=q))[:50]
        post_matches = [p.node for p in Post.objects.filter(body__icontains=q)][:50]
        bookmark_matches = [p.node for p in Bookmark.objects.filter(description__icontains=q)][:50]
        image_matches = [p.node for p in Image.objects.filter(description__icontains=q)][:50]
        nodes = uniquify(title_matches + post_matches + bookmark_matches + image_matches)
        nodes.sort(key=lambda x: x.created)
        nodes.reverse()
    return render_to_response("search_results.html",dict(q=q,nodes=nodes))



@login_required
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title","no title")
        body = request.POST.get("body","")
        tags = request.POST.get("tags","")
        user = get_object_or_404(Users,username=request.user.username)
        if request.POST.get("node_id","") == "":
            node = Node.objects.create(title=title,slug=make_slug(title),
                                       type="post",comments_allowed=True,
                                       user=user,status="Draft")
        else:
            node = get_object_or_404(Node,id=request.POST["node_id"])

        if request.POST.get("preview","") == "Preview":
            return render_to_response("add_post.html",dict(preview=True,node_id=node.id,title=title,body=body,tags=tags))
        else:
            node.set_tags(tags)
            node.title = title
            node.slug = make_slug(title)
            post = Post.objects.create(node=node,body=body,version=node.post_count() + 1,user=user,
                                       format="markdown")
            node.status = "Publish"
            node.save()
            return HttpResponseRedirect(node.get_absolute_url())
    return render_to_response("add_post.html",dict(preview=False,node_id=""))

def users(request):
    return render_to_response("users.html",dict(users=Users.objects.all()))

def user_index(request,username):
    user = get_object_or_404(Users,username=username)
    paginator = Paginator(user.newest_posts(),10)
    p = paginator.page(request.GET.get('page','1'))
    return render_to_response("user_index.html",dict(user=user,posts=p.object_list,paginator=p))

def user_type_index(request,username,type):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,status="Publish")
    years = uniquify([n.created.year for n in nodes])
    return render_to_response("user_type_index.html",dict(user=user,type=type,years=years))

def user_type_year_index(request,username,type,year):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,status="Publish",created__startswith="%04d" % int(year))
    months = uniquify([n.created.month for n in nodes])
    return render_to_response("user_type_year_index.html",dict(user=user,type=type,year=year,months=months))

def user_type_month_index(request,username,type,year,month):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,status="Publish",created__startswith="%04d-%02d" % (int(year),int(month)))
    days = uniquify([n.created.day for n in nodes])
    return render_to_response("user_type_month_index.html",dict(user=user,type=type,year=year,month=month,days=days))

def user_type_day_index(request,username,type,year,month,day):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,status="Publish",created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)))
    return render_to_response("user_type_day_index.html",dict(user=user,type=type,year=year,month=month,day=day,nodes=nodes))

def get_node_or_404(**kwargs):
    try:
        return get_object_or_404(Node,**kwargs)
    except django.core.exceptions.MultipleObjectsReturned:
        r = Node.objects.filter(user=kwargs['user'],type=kwargs['type'],
                                created__startswith=kwargs['created__startswith'],
                                slug=kwargs['slug'])
        return r[0]

def node(request,username,type,year,month,day,slug):
    user = get_object_or_404(Users,username=username)
    node = get_node_or_404(user=user,type=type,status="Publish",
                           created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)),
                           slug=slug)
    return render_to_response("node.html",dict(node=node))

def comment(request,username,type,year,month,day,slug,cyear,cmonth,cday,chour,cminute,csecond):
    user = get_object_or_404(Users,username=username)
    node = get_node_or_404(user=user,type=type,status="Publish",
                           created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)),
                           slug=slug)
    comment = get_object_or_404(Comment,node=node,
                                created__startswith="%04d-%02d-%02d %02d:%02d:%02d" % (int(cyear),int(cmonth),int(cday),int(chour),int(cminute),int(csecond)),
                                )
    return render_to_response("comment.html",dict(node=node,comment=comment))

def add_comment(request,username,type,year,month,day,slug):
    # some spammers submit reply_to with non-integers for some reason
    # so if we see that we can reject it immediately
    try:
        reply_to = int(request.POST.get('reply_to','0'))
    except ValueError:
        return HttpResponse("go away")
    
    user = get_object_or_404(Users,username=username)
    node = get_node_or_404(user=user,type=type,status="Publish",
                           created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)),
                           slug=slug)
    if not node.comments_allowed:
        return HttpResponse("sorry, no comments allowed on this one")
    url = request.POST.get("url","")
    if not url == "":
        if not url.startswith("http://"):
            url = "http://" + url
    if request.POST.get('name','') == "" or request.POST.get('email','') == "":
        return HttpResponse("name and email are required fields")

    if request.POST.get('content','') == "":
        return HttpResponse("no content in your comment")

    referer = request.META.get('HTTP_REFERER',node.get_absolute_url())
    if request.POST.get('submit','') != "submit comment":
        referer = request.POST.get('original_referer',referer)
        return render_to_response("preview.html",dict(node=node,name=request.POST['name'],
                                                      url = url,
                                                      original_referer=referer,
                                                      email = request.POST['email'],
                                                      content = request.POST['content'],
                                                      reply_to = int(request.POST.get('reply_to','0'))))
    
    # if referer doesn't end in "add_comment/", we know they didn't preview and are thus spam
    if not referer.endswith("add_comment/"):
        return HttpResponse("go away, spammer")
    referer = request.POST.get('original_referer','')
    if referer == '':
        return HttpResponse("go away, spammer")
    
    c = Comment(author_name=request.POST['name'],
                author_url = url,
                author_email = request.POST['email'],
                body = request.POST['content'],
                node = node,
                reply_to = int(request.POST.get('reply_to','0')))
    
    if not request.user.is_anonymous():
        c.status = "approved"
    c.save()
    if c.status == "pending":
        subject = "new comment on %s" % node.title
        message = """comment from: %s
            
------
%s
------

to approve or delete, go here:
http://thraxil.org/admin/abraxas/comment/%d/
            """ % (c.author_name,c.body,c.id)
        mail_managers(subject,message,fail_silently=False)
        return HttpResponse("your comment has been submitted and is pending moderator approval. <a href='%s'>return</a>" % referer)
    else:
        return HttpResponseRedirect(referer)

def fields(request):
    all_fields = MetaField.objects.all()
    seen = dict()
    ufields = []
    for f in all_fields:
        if f.field_name not in seen:
            ufields.append(f)
            seen[f.field_name] = 1
        
    return render_to_response("fields.html",dict(fields=ufields))

def field(request,name):
    all_fields = MetaField.objects.filter(field_name__iexact=name)
    seen = dict()
    ufields = []
    for f in all_fields:
        if f.field_value not in seen:
            ufields.append(f)
            seen[f.field_value] = 1

    return render_to_response("field.html",dict(fields=ufields,name=name))


def field_value(request,name,value):
    nodes = [f.node for f in MetaField.objects.filter(field_name__iexact=name,
                                                      field_value__iexact=value)]
    return render_to_response("field_value.html",dict(nodes=nodes,name=name,value=value))

def tags(request):
    tags = scaled_tags()
    return render_to_response("tags.html",dict(tags=tags))

def tag(request,tag):
    t = get_object_or_404(Tag,slug=tag)
    return render_to_response("tag.html",dict(tag=t))


