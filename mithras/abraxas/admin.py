from django.contrib import admin
from .models import Node, Image, Post, Bookmark, Comment, Users, MetaField, Tag


class NodeAdmin(admin.ModelAdmin):
    list_display = ("title", "created")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Node, NodeAdmin)


class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(Users, UsersAdmin)


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class BookmarkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bookmark, BookmarkAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'approved', 'author_name', 'preview', 'remove')
    list_filter = ('status',)


admin.site.register(Comment, CommentAdmin)


class MetaFieldAdmin(admin.ModelAdmin):
    pass


admin.site.register(MetaField, MetaFieldAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tag, TagAdmin)
