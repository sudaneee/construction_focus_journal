from django import forms
from django.forms import formset_factory
from website.models import (
    Volume, Issue, Article, Author, SiteSettings, ScopeTopic, ReviewStep, GuidelineItem, Submission,
)


class VolumeForm(forms.ModelForm):
    class Meta:
        model = Volume
        fields = ['volume_number', 'year', 'description']
        widgets = {
            'volume_number': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 1',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. 2024',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
            }),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['volume', 'issue_number', 'publication_date', 'description']
        widgets = {
            'volume': forms.Select(attrs={'class': 'form-select'}),
            'issue_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
            }),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'affiliation', 'email', 'biography']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'affiliation': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # 'authors' is excluded — handled by AuthorSlotFormSet in the view
        fields = [
            'title', 'slug', 'abstract', 'keywords',
            'volume', 'issue',
            'pdf_file', 'cover_image',
            'publication_date', 'doi',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_title'}),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auto-generated from title (or enter manually)',
            }),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'construction, sustainability, BIM, ...',
            }),
            'volume': forms.Select(attrs={'class': 'form-select'}),
            'issue': forms.Select(attrs={'class': 'form-select'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
            }),
            'doi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10.1000/xyz123',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['cover_image'].required = False
        self.fields['doi'].required = False
        self.fields['volume'].required = False
        self.fields['issue'].required = False


class AuthorSlotForm(forms.Form):
    """One ordered author slot — collected into AuthorSlotFormSet."""
    author = forms.ModelChoiceField(
        queryset=Author.objects.order_by('full_name'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='— Select author —',
    )


# extra=0: slot count is driven entirely by initial data passed in the view
AuthorSlotFormSet = formset_factory(AuthorSlotForm, extra=0)


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'department', 'faculty', 'institution', 'logo', 'issn', 'eissn',
            'contact_email', 'contact_phone', 'contact_address', 'contact_response_time',
            'footer_tagline', 'linkedin_url', 'researchgate_url', 'twitter_url', 'academia_url',
            'mission_text', 'frequency', 'language', 'access_type', 'review_type', 'publisher_name',
            'submission_fee', 'payment_instructions',
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'issn': forms.TextInput(attrs={'class': 'form-control'}),
            'eissn': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_response_time': forms.TextInput(attrs={'class': 'form-control'}),
            'footer_tagline': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'researchgate_url': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control'}),
            'academia_url': forms.URLInput(attrs={'class': 'form-control'}),
            'mission_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'access_type': forms.TextInput(attrs={'class': 'form-control'}),
            'review_type': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher_name': forms.TextInput(attrs={'class': 'form-control'}),
            'submission_fee': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. NGN 15,000'}),
            'payment_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ScopeTopicForm(forms.ModelForm):
    class Meta:
        model = ScopeTopic
        fields = ['name', 'short_name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ReviewStepForm(forms.ModelForm):
    class Meta:
        model = ReviewStep
        fields = ['name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class GuidelineItemForm(forms.ModelForm):
    class Meta:
        model = GuidelineItem
        fields = ['label', 'value', 'order']
        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SubmissionReviewForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['status', 'editor_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'editor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
