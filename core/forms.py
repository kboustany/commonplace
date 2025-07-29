from django import forms

from .models import Entry, Tag


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'title',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'name',
            'category',
        ]