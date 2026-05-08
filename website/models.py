from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Volume(models.Model):
    volume_number = models.PositiveIntegerField(unique=True)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-volume_number']

    def __str__(self):
        return f"Volume {self.volume_number} ({self.year})"

    def get_absolute_url(self):
        return reverse('website:volume_detail', kwargs={'volume_number': self.volume_number})


class Issue(models.Model):
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, related_name='issues')
    issue_number = models.PositiveIntegerField()
    publication_date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('volume', 'issue_number')
        ordering = ['volume', 'issue_number']

    def __str__(self):
        return f"Vol. {self.volume.volume_number}, Issue {self.issue_number}"

    def get_absolute_url(self):
        return reverse('website:issue_detail', kwargs={
            'volume_number': self.volume.volume_number,
            'issue_number': self.issue_number,
        })


class Author(models.Model):
    full_name = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=300)
    email = models.EmailField(blank=True)
    biography = models.TextField(blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class ArticleAuthor(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('article', 'author')


class Article(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    abstract = models.TextField()
    keywords = models.CharField(max_length=500, help_text='Comma-separated keywords')
    authors = models.ManyToManyField(Author, through='ArticleAuthor', related_name='articles')
    volume = models.ForeignKey(
        Volume, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles'
    )
    issue = models.ForeignKey(
        Issue, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles'
    )
    pdf_file = models.FileField(upload_to='pdfs/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    publication_date = models.DateField()
    doi = models.CharField(max_length=200, blank=True, verbose_name='DOI')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('website:article_detail', kwargs={'slug': self.slug})

    def get_keywords_list(self):
        return [k.strip() for k in self.keywords.split(',') if k.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
