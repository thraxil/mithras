from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from models import *
import django
from django.core.mail import mail_managers
from django.contrib.auth.decorators import login_required
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
    return render_to_response("index.html",dict(posts=newest_posts()))

def users(request):
    return render_to_response("users.html",dict(users=Users.objects.all()))

def user_index(request,username):
    user = get_object_or_404(Users,username=username)
    return render_to_response("user_index.html",dict(user=user,posts=user.newest_posts()))

def user_type_index(request,username,type):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type)
    years = uniquify([n.created.year for n in nodes])
    return render_to_response("user_type_index.html",dict(user=user,type=type,years=years))

def user_type_year_index(request,username,type,year):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,created__startswith="%04d" % int(year))
    months = uniquify([n.created.month for n in nodes])
    return render_to_response("user_type_year_index.html",dict(user=user,type=type,year=year,months=months))

def user_type_month_index(request,username,type,year,month):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,created__startswith="%04d-%02d" % (int(year),int(month)))
    days = uniquify([n.created.day for n in nodes])
    return render_to_response("user_type_month_index.html",dict(user=user,type=type,year=year,month=month,days=days))

def user_type_day_index(request,username,type,year,month,day):
    user = get_object_or_404(Users,username=username)
    nodes = Node.objects.filter(user=user,type=type,created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)))
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
    node = get_node_or_404(user=user,type=type,
                           created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)),
                           slug=slug)
    return render_to_response("node.html",dict(node=node))

def comment(request,username,type,year,month,day,slug,cyear,cmonth,cday,chour,cminute,csecond):
    user = get_object_or_404(Users,username=username)
    node = get_node_or_404(user=user,type=type,
                           created__startswith="%04d-%02d-%02d" % (int(year),int(month),int(day)),
                           slug=slug)
    comment = get_object_or_404(Comment,node=node,
                                created__startswith="%04d-%02d-%02d %02d:%02d:%02d" % (int(cyear),int(cmonth),int(cday),int(chour),int(cminute),int(csecond)),
                                )
    return render_to_response("comment.html",dict(node=node,comment=comment))

def add_comment(request,username,type,year,month,day,slug):
    user = get_object_or_404(Users,username=username)
    node = get_node_or_404(user=user,type=type,
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


