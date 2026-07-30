from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch
from django.contrib import messages

from .models import Volume, Issue, Article, Author, ScopeTopic, ReviewStep, GuidelineItem
from .forms import ContactForm, SubmissionForm

_ordered_authors = Prefetch('authors', queryset=Author.objects.order_by('articleauthor__order'))


def home(request):
    current_issue = (
        Issue.objects
        .select_related('volume')
        .order_by('-publication_date')
        .first()
    )
    current_issue_articles = []
    if current_issue:
        current_issue_articles = (
            current_issue.articles
            .select_related('volume', 'issue')
            .prefetch_related(_ordered_authors)
        )
    volumes = Volume.objects.prefetch_related('issues').all()[:4]
    stats = {
        'articles': Article.objects.count(),
        'volumes': Volume.objects.count(),
        'authors': Author.objects.count(),
    }
    return render(request, 'website/home.html', {
        'current_issue': current_issue,
        'current_issue_articles': current_issue_articles,
        'volumes': volumes,
        'stats': stats,
        'scope_topics': ScopeTopic.objects.all(),
    })


def about(request):
    return render(request, 'website/about.html', {
        'scope_topics': ScopeTopic.objects.all(),
        'review_steps': ReviewStep.objects.all(),
        'guideline_items': GuidelineItem.objects.all(),
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


def submit_paper(request):
    form = SubmissionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        submission = form.save()
        messages.success(
            request,
            'Thank you for your submission. Your reference number is '
            f'{submission.reference_code()} — please quote it in any correspondence. '
            'Our editorial team will review it and be in touch.',
        )
        return redirect('website:submit')
    return render(request, 'website/submit.html', {'form': form})
