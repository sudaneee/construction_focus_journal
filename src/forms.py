from django import forms
from django.forms import formset_factory
from website.models import Volume, Issue, Article, Author


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
