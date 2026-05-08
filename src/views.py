from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse

from website.models import Volume, Issue, Article, Author
from .forms import VolumeForm, IssueForm, ArticleForm, AuthorForm


# ── Authentication ────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('src:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'src:dashboard'))
        messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'src/login.html')


def logout_view(request):
    logout(request)
    return redirect('src:login')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    recent_articles = (
        Article.objects
        .select_related('volume', 'issue')
        .prefetch_related('authors')
        .order_by('-created_at')[:8]
    )
    return render(request, 'src/dashboard.html', {
        'total_volumes': Volume.objects.count(),
        'total_issues': Issue.objects.count(),
        'total_articles': Article.objects.count(),
        'total_authors': Author.objects.count(),
        'recent_articles': recent_articles,
    })


# ── Volumes ───────────────────────────────────────────────────────────────────

@login_required
def volume_list(request):
    query = request.GET.get('q', '').strip()
    qs = Volume.objects.prefetch_related('issues')
    if query:
        qs = qs.filter(
            Q(volume_number__icontains=query) | Q(year__icontains=query) | Q(description__icontains=query)
        )
    paginator = Paginator(qs, 15)
    return render(request, 'src/volumes/list.html', {
        'volumes': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def volume_create(request):
    form = VolumeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Volume created successfully.')
        return redirect('src:volume_list')
    return render(request, 'src/volumes/form.html', {'form': form, 'action': 'Create'})


@login_required
def volume_edit(request, pk):
    volume = get_object_or_404(Volume, pk=pk)
    form = VolumeForm(request.POST or None, instance=volume)
    if form.is_valid():
        form.save()
        messages.success(request, 'Volume updated successfully.')
        return redirect('src:volume_list')
    return render(request, 'src/volumes/form.html', {
        'form': form, 'action': 'Edit', 'object': volume,
    })


@login_required
def volume_delete(request, pk):
    volume = get_object_or_404(Volume, pk=pk)
    if request.method == 'POST':
        volume.delete()
        messages.success(request, 'Volume deleted successfully.')
        return redirect('src:volume_list')
    return render(request, 'src/confirm_delete.html', {
        'object': volume, 'object_type': 'Volume', 'cancel_url': reverse('src:volume_list'),
    })


# ── Issues ────────────────────────────────────────────────────────────────────

@login_required
def issue_list(request):
    query = request.GET.get('q', '').strip()
    qs = Issue.objects.select_related('volume')
    if query:
        qs = qs.filter(
            Q(issue_number__icontains=query) |
            Q(volume__volume_number__icontains=query) |
            Q(volume__year__icontains=query)
        )
    paginator = Paginator(qs, 15)
    return render(request, 'src/issues/list.html', {
        'issues': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def issue_create(request):
    form = IssueForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Issue created successfully.')
        return redirect('src:issue_list')
    return render(request, 'src/issues/form.html', {'form': form, 'action': 'Create'})


@login_required
def issue_edit(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    form = IssueForm(request.POST or None, instance=issue)
    if form.is_valid():
        form.save()
        messages.success(request, 'Issue updated successfully.')
        return redirect('src:issue_list')
    return render(request, 'src/issues/form.html', {
        'form': form, 'action': 'Edit', 'object': issue,
    })


@login_required
def issue_delete(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        issue.delete()
        messages.success(request, 'Issue deleted successfully.')
        return redirect('src:issue_list')
    return render(request, 'src/confirm_delete.html', {
        'object': issue, 'object_type': 'Issue', 'cancel_url': reverse('src:issue_list'),
    })


# ── Articles ──────────────────────────────────────────────────────────────────

@login_required
def article_list(request):
    query = request.GET.get('q', '').strip()
    qs = Article.objects.select_related('volume', 'issue').prefetch_related('authors')
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(keywords__icontains=query) |
            Q(authors__full_name__icontains=query)
        ).distinct()
    paginator = Paginator(qs, 15)
    return render(request, 'src/articles/list.html', {
        'articles': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def article_create(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Article created successfully.')
        return redirect('src:article_list')
    return render(request, 'src/articles/form.html', {'form': form, 'action': 'Create'})


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        form.save()
        messages.success(request, 'Article updated successfully.')
        return redirect('src:article_list')
    return render(request, 'src/articles/form.html', {
        'form': form, 'action': 'Edit', 'object': article,
    })


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully.')
        return redirect('src:article_list')
    return render(request, 'src/confirm_delete.html', {
        'object': article, 'object_type': 'Article', 'cancel_url': reverse('src:article_list'),
    })


# ── Authors ───────────────────────────────────────────────────────────────────

@login_required
def author_list(request):
    query = request.GET.get('q', '').strip()
    qs = Author.objects.all()
    if query:
        qs = qs.filter(
            Q(full_name__icontains=query) |
            Q(affiliation__icontains=query) |
            Q(email__icontains=query)
        )
    paginator = Paginator(qs, 15)
    return render(request, 'src/authors/list.html', {
        'authors': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Author created successfully.')
        return redirect('src:author_list')
    return render(request, 'src/authors/form.html', {'form': form, 'action': 'Create'})


@login_required
def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        form.save()
        messages.success(request, 'Author updated successfully.')
        return redirect('src:author_list')
    return render(request, 'src/authors/form.html', {
        'form': form, 'action': 'Edit', 'object': author,
    })


@login_required
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        messages.success(request, 'Author deleted successfully.')
        return redirect('src:author_list')
    return render(request, 'src/confirm_delete.html', {
        'object': author, 'object_type': 'Author', 'cancel_url': reverse('src:author_list'),
    })
