from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    search_fields = ('title',)
    # prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text')
    search_fields = ('post', 'author',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('following', 'user')
    search_fields = ('following', 'user')


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
