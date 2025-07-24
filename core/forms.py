from django import forms

from .models import (
    Category,
    Entry,
    Tag,
    PlainItem,
)


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'name',
            'description'
        ]
        labels = {
            'name': 'Name',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'category',
            'name',
        ]
        labels = {
            'category': 'Category', 
            'name': 'Name',
        }
        widgets = {
            'category': forms.Select(choices=Category.objects.all()),
        }


class PlainForm(forms.ModelForm):
    class Meta:
        model = PlainItem
        fields = [
            'name',
            'body',
        ]
        labels = {
            'name': 'Name',
            'body': 'Body',
        }
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80}),
        }