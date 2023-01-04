from django.contrib import admin
from .models import Post, Comment, Tag


class CommentInLine(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'tags', 'created', 'publish', 'author')
    search_fields = ('title', 'body', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    ordering = ('-status', '-publish')
    inlines = [CommentInLine]
# admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    search_fields = ('tag_name',)
