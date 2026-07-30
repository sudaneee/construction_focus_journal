from django.contrib import admin
from .models import (
    Volume, Issue, Author, Article, ArticleAuthor, SiteSettings,
    ScopeTopic, ReviewStep, GuidelineItem, Submission,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Identity', {'fields': ['site_name', 'department', 'faculty', 'institution', 'logo', 'issn', 'eissn']}),
        ('Contact', {'fields': ['contact_email', 'contact_phone', 'contact_address', 'contact_response_time']}),
        ('Footer & Social', {'fields': ['footer_tagline', 'linkedin_url', 'researchgate_url', 'twitter_url', 'academia_url']}),
        ('About Page', {'fields': ['mission_text', 'frequency', 'language', 'access_type', 'review_type', 'publisher_name']}),
        ('Submission & Payment', {'fields': ['submission_fee', 'payment_instructions']}),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ScopeTopic)
class ScopeTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'order']
    list_editable = ['order']
    ordering = ['order']


@admin.register(ReviewStep)
class ReviewStepAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    ordering = ['order']


@admin.register(GuidelineItem)
class GuidelineItemAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order']
    list_editable = ['order']
    ordering = ['order']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'corresponding_author_name', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['title', 'corresponding_author_name', 'corresponding_author_email']
    readonly_fields = ['submitted_at', 'updated_at']
    date_hierarchy = 'submitted_at'


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


class ArticleAuthorInline(admin.TabularInline):
    model = ArticleAuthor
    extra = 1
    fields = ['order', 'author']
    ordering = ['order']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'volume', 'issue', 'publication_date', 'doi', 'is_featured']
    list_filter = ['volume', 'issue', 'publication_date', 'is_featured']
    search_fields = ['title', 'abstract', 'keywords']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleAuthorInline]
    date_hierarchy = 'publication_date'
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {'fields': ['title', 'slug', 'abstract', 'keywords']}),
        ('Classification', {'fields': ['volume', 'issue']}),
        ('Files', {'fields': ['pdf_file', 'cover_image']}),
        ('Publication', {'fields': ['publication_date', 'doi', 'is_featured']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
