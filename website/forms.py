from django import forms
from django.core.validators import FileExtensionValidator

from .models import Submission

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com',
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Your message...',
        })
    )


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            'title', 'abstract', 'keywords',
            'corresponding_author_name', 'corresponding_author_email',
            'corresponding_author_affiliation', 'corresponding_author_phone',
            'manuscript_file', 'payment_receipt',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manuscript Title'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Abstract (150–250 words)'}),
            'keywords': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'construction, sustainability, BIM, ...',
            }),
            'corresponding_author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'corresponding_author_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'corresponding_author_affiliation': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Institution / Organisation',
            }),
            'corresponding_author_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'manuscript_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'payment_receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['corresponding_author_phone'].required = False

    def _clean_file(self, field_name, extensions):
        f = self.cleaned_data.get(field_name)
        if not f:
            return f
        validator = FileExtensionValidator(allowed_extensions=extensions)
        validator(f)
        if f.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File must be smaller than 10MB.')
        return f

    def clean_manuscript_file(self):
        return self._clean_file('manuscript_file', ['pdf', 'doc', 'docx'])

    def clean_payment_receipt(self):
        return self._clean_file('payment_receipt', ['pdf', 'jpg', 'jpeg', 'png'])
