from django import forms

from .models import Entry, ItemType, Tag
from .models import Letter, Paragraph, Quotation, Recipe, Technical


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'title',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 80}
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'name',
            'category',
        ]
        

class ItemTypeForm(forms.Form):
    item_type = forms.ChoiceField(
        choices=ItemType.choices,
        label='Select the type of item to create.',
        required=True,
    )


class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = [
            'title',
            'body',
        ]
        widgets = {
            'body': forms.Textarea(
                attrs={'cols': 80}
            ),
        }


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = [
            'title',
            'description',
            'body',
            'author',
        ]
        labels = {
            'body': 'Quotation',
        }
        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 80, 'placeholder': 'Description (optional)'}
            ),
            'body': forms.Textarea(
                attrs={'cols': 80}
            ),
        }


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = [
            'title',
            'description',
            'date',
            'address',
            'location',
            'salutation',
            'body',
            'closing',
            'signature',
            'postscript',
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 80, 'placeholder': 'Description (optional)'}
            ),
            'date': forms.TextInput(
                attrs={'placeholder': 'Date (optional)'}
            ),
            'address': forms.TextInput(
                attrs={'placeholder': 'Address (optional)'}
            ),
            'location': forms.TextInput(
                attrs={'placeholder': 'Location (optional)'}
            ),
            'salutation': forms.TextInput(
                attrs={'placeholder': 'Salutation (optional)'}
            ),
            'body': forms.Textarea(
                attrs={'cols': 80}
            ),
            'closing': forms.TextInput(
                attrs={'placeholder': 'Closing (optional)'}
            ),
            'signature': forms.TextInput(
                attrs={'placeholder': 'Signature (optional)'}
            ),
            'postscript': forms.Textarea(
                attrs={'cols': 80, 'placeholder': 'Postscript (optional)'}
            ),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'time',
            'servings',
            'ingredients',
            'directions',
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 80, 'placeholder': 'Description (optional)'}
            ),
            'time': forms.TextInput(
                attrs={'placeholder': 'Time (optional)'}
            ),
            'servings': forms.TextInput(
                attrs={'placeholder': 'Servings (optional)'}
            ),
        }


class TechnicalForm(forms.ModelForm):
    class Meta:
        model = Technical
        fields = [
            'title',
            'description',
            'body',
        ]
        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 80, 'placeholder': 'Description (optional)'}
            ),
            'body': forms.Textarea(
                attrs={'cols': 80}
            ),
        }


ITEM_FORMS = {
    Paragraph.type_key: ParagraphForm,
    Quotation.type_key: QuotationForm,
    Letter.type_key: LetterForm,
    Recipe.type_key: RecipeForm,
    Technical.type_key: TechnicalForm,
}