from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch
from django.contrib import messages

from .models import Volume, Issue, Article, Author
from .forms import ContactForm

_ordered_authors = Prefetch('authors', queryset=Author.objects.order_by('articleauthor__order'))

SCOPE_TOPICS = [
    'Construction Management',
    'Structural Engineering',
    'Sustainable Building',
    'Project Management',
    'BIM & Digital Construction',
    'Infrastructure Development',
    'Materials & Methods',
    'Health & Safety',
]

SCOPE_TOPICS_FULL = [
    'Construction Management & Economics',
    'Structural Engineering & Analysis',
    'Sustainable Building & Green Construction',
    'Project Planning & Scheduling',
    'Building Information Modelling (BIM)',
    'Infrastructure Development & Transport',
    'Construction Materials & Testing',
    'Health & Safety on Site',
    'Smart Technologies in Construction',
    'Environmental Impact Assessment',
]


def home(request):
    latest_articles = (
        Article.objects
        .select_related('volume', 'issue')
        .prefetch_related(_ordered_authors)[:6]
    )
    volumes = Volume.objects.prefetch_related('issues').all()[:4]
    stats = {
        'articles': Article.objects.count(),
        'volumes': Volume.objects.count(),
        'authors': Author.objects.count(),
    }
    return render(request, 'website/home.html', {
        'latest_articles': latest_articles,
        'volumes': volumes,
        'stats': stats,
        'scope_topics': SCOPE_TOPICS,
    })


REVIEW_STEPS = [
    'Submission Received',
    'Initial Editorial Screening',
    'Double-Blind Peer Review',
    'Author Revision',
    'Final Decision',
    'Publication',
]


def about(request):
    return render(request, 'website/about.html', {
        'scope_topics': SCOPE_TOPICS_FULL,
        'review_steps': REVIEW_STEPS,
    })


def volumes_list(request):
    volumes = Volume.objects.prefetch_related('issues').all()
    return render(request, 'website/volumes.html', {'volumes': volumes})


def volume_detail(request, volume_number):
    volume = get_object_or_404(Volume, volume_number=volume_number)
    issues = volume.issues.all()
    return render(request, 'website/volume_detail.html', {
        'volume': volume,
        'issues': issues,
    })


def issue_detail(request, volume_number, issue_number):
    volume = get_object_or_404(Volume, volume_number=volume_number)
    issue = get_object_or_404(Issue, volume=volume, issue_number=issue_number)
    articles = (
        issue.articles
        .select_related('volume', 'issue')
        .prefetch_related(_ordered_authors)
    )
    return render(request, 'website/issue_detail.html', {
        'volume': volume,
        'issue': issue,
        'articles': articles,
    })


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('volume', 'issue').prefetch_related(_ordered_authors),
        slug=slug,
    )
    related = (
        Article.objects
        .filter(issue=article.issue)
        .exclude(pk=article.pk)
        .select_related('volume', 'issue')
        .prefetch_related(_ordered_authors)[:4]
    ) if article.issue else []
    return render(request, 'website/article_detail.html', {
        'article': article,
        'related': related,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = (
            Article.objects
            .filter(
                Q(title__icontains=query) |
                Q(abstract__icontains=query) |
                Q(keywords__icontains=query) |
                Q(authors__full_name__icontains=query)
            )
            .select_related('volume', 'issue')
            .prefetch_related(_ordered_authors)
            .distinct()
        )
    return render(request, 'website/search.html', {
        'query': query,
        'results': results,
    })


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        messages.success(
            request,
            'Thank you for reaching out. We will get back to you shortly.',
        )
        return redirect('website:contact')
    return render(request, 'website/contact.html', {'form': form})
