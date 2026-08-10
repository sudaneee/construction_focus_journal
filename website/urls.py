from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('volumes/', views.volumes_list, name='volumes'),
    path('volumes/<int:volume_number>/', views.volume_detail, name='volume_detail'),
    path('volumes/<int:volume_number>/issues/<int:issue_number>/', views.issue_detail, name='issue_detail'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('announcements/', views.announcements_list, name='announcements'),
    path('announcements/<slug:slug>/', views.announcement_detail, name='announcement_detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('submit/', views.submit_paper, name='submit'),
]
