from django.contrib import admin
from .models import Volume, Issue, Author, Article


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0
    fields = ['issue_number', 'publication_date', 'description']


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ['volume_number', 'year', 'issue_count', 'article_count']
    inlines = [IssueInline]

    def issue_count(self, obj):
        return obj.issues.count()
    issue_count.short_description = 'Issues'

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'volume', 'issue_number', 'publication_date', 'article_count']
    list_filter = ['volume']
    date_hierarchy = 'publication_date'

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'affiliation', 'email', 'article_count']
    search_fields = ['full_name', 'affiliation', 'email']

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'volume', 'issue', 'publication_date', 'doi']
    list_filter = ['volume', 'issue', 'publication_date']
    search_fields = ['title', 'abstract', 'keywords']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['authors']
    date_hierarchy = 'publication_date'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {'fields': ['title', 'slug', 'abstract', 'keywords']}),
        ('Classification', {'fields': ['volume', 'issue', 'authors']}),
        ('Files', {'fields': ['pdf_file', 'cover_image']}),
        ('Publication', {'fields': ['publication_date', 'doi']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
