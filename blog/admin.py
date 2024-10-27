from django.contrib import admin
from blog.models import Posts, Category


class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at', 'published_at')
    search_fields = ('title', 'content')
    list_filter = ('status', 'created_at', 'updated_at', 'published_at')
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Posts, PostsAdmin)
admin.site.register(Category, CategoryAdmin)
