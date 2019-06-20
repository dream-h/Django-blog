from django.contrib import admin
from . import models


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('nid', 'username', 'password', 'nickname')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'site', 'theme', 'user')


class TagAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'blog')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nid', 'title', 'category')


admin.site.register(models.UserInfo, UserInfoAdmin)
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Tag, TagAdmin)
