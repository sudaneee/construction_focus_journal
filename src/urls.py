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
]
