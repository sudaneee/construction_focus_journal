from django.urls import path
from . import views

app_name = 'src'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Volumes
    path('volumes/', views.volume_list, name='volume_list'),
    path('volumes/create/', views.volume_create, name='volume_create'),
    path('volumes/<int:pk>/edit/', views.volume_edit, name='volume_edit'),
    path('volumes/<int:pk>/delete/', views.volume_delete, name='volume_delete'),

    # Issues
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/create/', views.issue_create, name='issue_create'),
    path('issues/<int:pk>/edit/', views.issue_edit, name='issue_edit'),
    path('issues/<int:pk>/delete/', views.issue_delete, name='issue_delete'),

    # Articles
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),

    # Authors
    path('authors/', views.author_list, name='author_list'),
    path('authors/create/', views.author_create, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),

    # Submissions
    path('submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'),
    path('submissions/<int:pk>/delete/', views.submission_delete, name='submission_delete'),

    # Site Settings
    path('settings/', views.site_settings_edit, name='site_settings_edit'),

    # Scope Topics
    path('scope-topics/', views.scope_topic_list, name='scope_topic_list'),
    path('scope-topics/create/', views.scope_topic_create, name='scope_topic_create'),
    path('scope-topics/<int:pk>/edit/', views.scope_topic_edit, name='scope_topic_edit'),
    path('scope-topics/<int:pk>/delete/', views.scope_topic_delete, name='scope_topic_delete'),

    # Review Steps
    path('review-steps/', views.review_step_list, name='review_step_list'),
    path('review-steps/create/', views.review_step_create, name='review_step_create'),
    path('review-steps/<int:pk>/edit/', views.review_step_edit, name='review_step_edit'),
    path('review-steps/<int:pk>/delete/', views.review_step_delete, name='review_step_delete'),

    # Author Guidelines
    path('guidelines/', views.guideline_item_list, name='guideline_item_list'),
    path('guidelines/create/', views.guideline_item_create, name='guideline_item_create'),
    path('guidelines/<int:pk>/edit/', views.guideline_item_edit, name='guideline_item_edit'),
    path('guidelines/<int:pk>/delete/', views.guideline_item_delete, name='guideline_item_delete'),
]
