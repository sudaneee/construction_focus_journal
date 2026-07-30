from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.urls import reverse

from website.models import (
    Volume, Issue, Article, Author, ArticleAuthor, SiteSettings,
    ScopeTopic, ReviewStep, GuidelineItem, Submission,
)
from .forms import (
    VolumeForm, IssueForm, ArticleForm, AuthorForm, AuthorSlotFormSet,
    SiteSettingsForm, ScopeTopicForm, ReviewStepForm, GuidelineItemForm, SubmissionReviewForm,
)

# Reusable prefetch that returns authors in defined position order
_ordered_authors = Prefetch('authors', queryset=Author.objects.order_by('articleauthor__order'))


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
        .prefetch_related(_ordered_authors)
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
    qs = Article.objects.select_related('volume', 'issue').prefetch_related(_ordered_authors)
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


def _author_initial(article):
    """Build initial data list for AuthorSlotFormSet from existing article authors."""
    existing = (
        ArticleAuthor.objects
        .filter(article=article)
        .order_by('order')
        .values_list('author_id', flat=True)
    )
    return [{'author': aid} for aid in existing] + [{}]


@login_required
def article_create(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    # Default 3 empty slots for new articles
    initial = [{}, {}, {}]
    formset = AuthorSlotFormSet(request.POST or None, prefix='authors', initial=initial)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        article = form.save()
        order = 0
        for f in formset.forms:
            if not f.cleaned_data:
                continue
            author = f.cleaned_data.get('author')
            if author:
                ArticleAuthor.objects.create(article=article, author=author, order=order)
                order += 1
        messages.success(request, 'Article created successfully.')
        return redirect('src:article_list')
    return render(request, 'src/articles/form.html', {
        'form': form, 'formset': formset, 'action': 'Create',
    })


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    initial = _author_initial(article)
    formset = AuthorSlotFormSet(request.POST or None, prefix='authors', initial=initial)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        ArticleAuthor.objects.filter(article=article).delete()
        order = 0
        for f in formset.forms:
            if not f.cleaned_data:
                continue
            author = f.cleaned_data.get('author')
            if author:
                ArticleAuthor.objects.create(article=article, author=author, order=order)
                order += 1
        messages.success(request, 'Article updated successfully.')
        return redirect('src:article_list')
    return render(request, 'src/articles/form.html', {
        'form': form, 'formset': formset, 'action': 'Edit', 'object': article,
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


# ── Site Settings ─────────────────────────────────────────────────────────────

@login_required
def site_settings_edit(request):
    settings_obj = SiteSettings.load()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=settings_obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Site settings updated successfully.')
        return redirect('src:site_settings_edit')
    return render(request, 'src/settings/form.html', {'form': form})


# ── Scope Topics ──────────────────────────────────────────────────────────────

@login_required
def scope_topic_list(request):
    query = request.GET.get('q', '').strip()
    qs = ScopeTopic.objects.all()
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(short_name__icontains=query))
    paginator = Paginator(qs, 15)
    return render(request, 'src/scope_topics/list.html', {
        'scope_topics': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def scope_topic_create(request):
    form = ScopeTopicForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Scope topic created successfully.')
        return redirect('src:scope_topic_list')
    return render(request, 'src/scope_topics/form.html', {'form': form, 'action': 'Create'})


@login_required
def scope_topic_edit(request, pk):
    topic = get_object_or_404(ScopeTopic, pk=pk)
    form = ScopeTopicForm(request.POST or None, instance=topic)
    if form.is_valid():
        form.save()
        messages.success(request, 'Scope topic updated successfully.')
        return redirect('src:scope_topic_list')
    return render(request, 'src/scope_topics/form.html', {
        'form': form, 'action': 'Edit', 'object': topic,
    })


@login_required
def scope_topic_delete(request, pk):
    topic = get_object_or_404(ScopeTopic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Scope topic deleted successfully.')
        return redirect('src:scope_topic_list')
    return render(request, 'src/confirm_delete.html', {
        'object': topic, 'object_type': 'Scope Topic', 'cancel_url': reverse('src:scope_topic_list'),
    })


# ── Review Steps ──────────────────────────────────────────────────────────────

@login_required
def review_step_list(request):
    query = request.GET.get('q', '').strip()
    qs = ReviewStep.objects.all()
    if query:
        qs = qs.filter(name__icontains=query)
    paginator = Paginator(qs, 15)
    return render(request, 'src/review_steps/list.html', {
        'review_steps': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def review_step_create(request):
    form = ReviewStepForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Review step created successfully.')
        return redirect('src:review_step_list')
    return render(request, 'src/review_steps/form.html', {'form': form, 'action': 'Create'})


@login_required
def review_step_edit(request, pk):
    step = get_object_or_404(ReviewStep, pk=pk)
    form = ReviewStepForm(request.POST or None, instance=step)
    if form.is_valid():
        form.save()
        messages.success(request, 'Review step updated successfully.')
        return redirect('src:review_step_list')
    return render(request, 'src/review_steps/form.html', {
        'form': form, 'action': 'Edit', 'object': step,
    })


@login_required
def review_step_delete(request, pk):
    step = get_object_or_404(ReviewStep, pk=pk)
    if request.method == 'POST':
        step.delete()
        messages.success(request, 'Review step deleted successfully.')
        return redirect('src:review_step_list')
    return render(request, 'src/confirm_delete.html', {
        'object': step, 'object_type': 'Review Step', 'cancel_url': reverse('src:review_step_list'),
    })


# ── Author Guidelines ─────────────────────────────────────────────────────────

@login_required
def guideline_item_list(request):
    query = request.GET.get('q', '').strip()
    qs = GuidelineItem.objects.all()
    if query:
        qs = qs.filter(Q(label__icontains=query) | Q(value__icontains=query))
    paginator = Paginator(qs, 15)
    return render(request, 'src/guidelines/list.html', {
        'guidelines': paginator.get_page(request.GET.get('page')),
        'query': query,
    })


@login_required
def guideline_item_create(request):
    form = GuidelineItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Guideline created successfully.')
        return redirect('src:guideline_item_list')
    return render(request, 'src/guidelines/form.html', {'form': form, 'action': 'Create'})


@login_required
def guideline_item_edit(request, pk):
    item = get_object_or_404(GuidelineItem, pk=pk)
    form = GuidelineItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, 'Guideline updated successfully.')
        return redirect('src:guideline_item_list')
    return render(request, 'src/guidelines/form.html', {
        'form': form, 'action': 'Edit', 'object': item,
    })


@login_required
def guideline_item_delete(request, pk):
    item = get_object_or_404(GuidelineItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Guideline deleted successfully.')
        return redirect('src:guideline_item_list')
    return render(request, 'src/confirm_delete.html', {
        'object': item, 'object_type': 'Guideline', 'cancel_url': reverse('src:guideline_item_list'),
    })


# ── Submissions ───────────────────────────────────────────────────────────────

@login_required
def submission_list(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    qs = Submission.objects.all()
    if status:
        qs = qs.filter(status=status)
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(corresponding_author_name__icontains=query) |
            Q(corresponding_author_email__icontains=query)
        )
    paginator = Paginator(qs, 15)
    return render(request, 'src/submissions/list.html', {
        'submissions': paginator.get_page(request.GET.get('page')),
        'query': query,
        'status': status,
        'status_choices': Submission.STATUS_CHOICES,
    })


@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    form = SubmissionReviewForm(request.POST or None, instance=submission)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Submission updated successfully.')
        return redirect('src:submission_detail', pk=submission.pk)
    return render(request, 'src/submissions/detail.html', {
        'submission': submission,
        'form': form,
    })


@login_required
def submission_delete(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.method == 'POST':
        submission.delete()
        messages.success(request, 'Submission deleted successfully.')
        return redirect('src:submission_list')
    return render(request, 'src/confirm_delete.html', {
        'object': submission, 'object_type': 'Submission', 'cancel_url': reverse('src:submission_list'),
    })
