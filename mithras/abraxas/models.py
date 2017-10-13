from django.db import models
import re
from django.template.loader import get_template
import math


class Users(models.Model):
    username = models.CharField(unique=True, max_length=128)
    email = models.CharField(max_length=256)
    fullname = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    bio = models.TextField()
    css = models.TextField()

    class Meta:
        db_table = u'users'

    def __str__(self):
        return self.username + " (" + self.fullname + ")"

    def get_absolute_url(self):
        return "/users/%s/" % self.username

    def newest_posts(self):
        return Node.objects.filter(
            type="post",
            status="Publish",
            user=self).order_by("-created")


class Tag(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()

    def get_absolute_url(self):
        return "/tags/%s/" % self.slug

    def __str__(self):
        return self.name

    def clear_if_empty(self):
        if self.node_set.all().count() == 0:
            self.delete()


def make_slug(title="no title"):
    title = title.strip()
    slug = re.sub(r"[\W\-]+", "-", title)
    slug = re.sub(r"^\-+", "", slug)
    slug = re.sub(r"\-+$", "", slug)
    if slug == "":
        slug = "-"
    return slug


def get_or_create_tag(name):
    r = Tag.objects.filter(slug__iexact=make_slug(name))
    if r.count() > 0:
        return r[0]
    else:
        return Tag.objects.create(name=name, slug=make_slug(name))


def tag_cloud():
    """ eventually, we'll scale the cloud. for now,
    just return list of all tags """
    return Tag.objects.all().order_by("name")


def clear_unused_tags():
    for t in Tag.objects.all():
        t.clear_if_empty()


class Node(models.Model):
    slug = models.CharField(max_length=256, db_index=True)
    status = models.CharField(max_length=7, db_index=True)
    comments_allowed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users)
    type = models.CharField(max_length=8, db_index=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        db_table = u'node'

    def __str__(self):
        return self.title

    def p(self):
        return Post.objects.filter(node=self).order_by("-version").first()

    def b(self):
        return Bookmark.objects.filter(node=self).order_by("-version").first()

    def i(self):
        return Image.objects.filter(node=self).order_by("-version").first()

    def get_absolute_url(self):
        return "/users/%s/%ss/%04d/%02d/%02d/%s/" % (
            self.user.username, self.type,
            self.created.year, self.created.month,
            self.created.day, self.slug)

    def is_post(self):
        return self.type == "post"

    def is_bookmark(self):
        return self.type == "bookmark"

    def is_image(self):
        return self.type == "image"

    def has_comments(self):
        return self.comment_set.filter(status='approved').count() > 0

    def num_comments(self):
        return self.comment_set.filter(status='approved').count()

    def top_level_comments(self):
        return self.comment_set.filter(
            reply_to=0, status='approved').order_by("created")

    def has_tags(self):
        return self.tags.all().count() > 0

    def get_tags(self):
        return self.tags.all()

    def tags_string(self):
        return ", ".join([t.name.lower() for t in self.tags.all()])

    def set_tags(self, tags_string):
        NodeTagger(self).set_tags(tags_string)

    def add_tag(self, tagstring):
        NodeTagger(self).add_tag(tagstring)

    def add_tag_from_string(self, tag):
        NodeTagger(self).add_tag_from_string(tag)

    def post_count(self):
        return Post.objects.filter(node=self).all().count()

    def touch(self):
        pass

    def update_post(self, title, body, user, tags):
        Post.objects.create(node=self, body=body,
                            version=self.post_count() + 1, user=user,
                            format="markdown")
        self.set_tags(tags)
        self.title = title
        self.status = "Publish"
        self.save()


class NodeTagger(object):
    def __init__(self, node):
        self.node = node

    def set_tags(self, tags_string):
        self.node.tags.clear()
        for tag in tags_string.split(", "):
            self.add_tag_from_string(tag)
        clear_unused_tags()
        return

    def add_tag(self, tagstring):
        tag = get_or_create_tag(tagstring)
        if tag not in self.node.get_tags():
            self.node.tags.add(tag)
            self.node.save()

    def add_tag_from_string(self, tag):
        tag = tag.lower().strip()
        if not tag:
            return
        t = get_or_create_tag(tag)
        self.node.tags.add(t)


def class_from_weight(w, thresholds):
    matches = [p[0] for p in enumerate(thresholds)
               if p[1] <= w]
    if len(matches) > 0:
        return matches[-1] + 1
    return 1


def ex_weights(l):
    return [int(w) for (t, w) in l]


def scaled_tags():
    if Tag.objects.all().count() < 1:
        return

    levels = 5

    tags = [(t, t.node_set.all().count())
            for t in Tag.objects.all().order_by("name")
            if t.node_set.all().count() > 0]
    max_weight = max(ex_weights(tags))
    min_weight = min(ex_weights(tags))

    thresholds = [math.pow(max_weight - min_weight + 1,
                           float(i) / float(levels))
                  for i in range(0, levels)]

    for (t, w) in tags:
        c = class_from_weight(w, thresholds)
        t.weight = c
        yield t


class MetaField(models.Model):
    node = models.ForeignKey(Node)
    field_value = models.CharField(max_length=256)
    field_name = models.CharField(max_length=256)

    class Meta:
        db_table = u'meta_field'

    def __str__(self):
        return "%s: %s" % (self.field_name, self.field_value)


class Post(models.Model):
    node = models.ForeignKey(Node)
    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)
    version = models.IntegerField()
    user = models.ForeignKey(Users)
    format = models.CharField(max_length=256)

    class Meta:
        db_table = u'post'

    def __str__(self):
        return self.node.title


class Bookmark(models.Model):
    node = models.ForeignKey(Node)
    description = models.TextField()
    url = models.CharField(max_length=256)
    via_name = models.CharField(max_length=256)
    modified = models.DateTimeField(auto_now=True)
    version = models.IntegerField()
    via_url = models.CharField(max_length=256)
    user = models.ForeignKey(Users)
    format = models.CharField(max_length=256)

    class Meta:
        db_table = u'bookmark'

    def __str__(self):
        return self.node.title


class Image(models.Model):
    node = models.ForeignKey(Node)
    description = models.TextField(blank=True, default="")
    thumb_width = models.IntegerField()
    thumb_height = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()
    ext = models.CharField(max_length=3)
    version = models.IntegerField()
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users)
    format = models.CharField(max_length=256)
    rhash = models.CharField(max_length=256, default="")

    class Meta:
        db_table = u'image'

    def __str__(self):
        return "Image %d - Node %d - %s" % (self.id, self.node.id,
                                            self.node.title)

    def scaled_image_url(self):
        if self.rhash != "":
            return ("https://d2f33fmhbh7cs9.cloudfront.net/"
                    "image/%s/full/%d.%s" % (
                        self.rhash, self.node.id, self.ext))
        else:
            sid = "%05d" % self.node.id
            p = "/".join(list(sid))
            return ("http://static.thraxil.org/pomelo_images/"
                    "scaled/%s/%d.%s" % (
                        p, self.node.id, self.ext))


class Comment(models.Model):
    node = models.ForeignKey(Node)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author_email = models.CharField(max_length=256, blank=True)
    author_name = models.CharField(max_length=256, blank=True)
    author_url = models.CharField(max_length=256, blank=True)
    reply_to = models.IntegerField()
    status = models.CharField(max_length=30, default="pending",
                              choices=(('pending', 'Pending Moderation'),
                                       ('approved', 'Approved')))

    class Meta:
        db_table = u'comment'

    def __str__(self):
        return "Re: %s: by %s at %s" % (self.node.title,
                                        self.author_name,
                                        str(self.created))

    def remove(self):
        return ('<input type="button" value="Delete" '
                'onclick="location.href=\'%s/delete/\'"'
                '/>') % (self.pk)
    remove.short_description = ''
    remove.allow_tags = True

    def preview(self):
        return self.body[:30]

    def approved(self):
        return self.status == 'approved'
    approved.boolean = True

    def timestampdir(self):
        return "%04d-%02d-%02d-%02d-%02d-%02d/" % (
            self.created.year, self.created.month, self.created.day,
            self.created.hour, self.created.minute, self.created.second)

    def get_absolute_url(self):
        return self.node.get_absolute_url() + "comments/" + self.timestampdir()

    def has_replies(self):
        return self.node.comment_set.filter(reply_to=self.id,
                                            status='approved').count() > 0

    def replies(self):
        return self.node.comment_set.filter(reply_to=self.id,
                                            status='approved')

    def replies_html(self):
        chunks = []
        for reply in self.replies():
            template = get_template("abraxas/replies.html")
            c = dict(comment=reply)
            chunks.append(template.render(c))
        return "".join(chunks)

    def has_author_url(self):
        # people put stupid shit into the url field
        if self.author_url == "" or self.author_url == "http://":
            return False
        return self.author_url.startswith("http://")


def newest_posts():
    return Node.objects.filter(type="post",
                               status="Publish").order_by("-created")


def all_pending_comments():
    return Comment.objects.filter(status="pending").order_by("-created")
