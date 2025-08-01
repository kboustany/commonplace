from django.contrib.auth.models import User
from django.db import models

from polymorphic.models import PolymorphicModel


class Entry(models.Model):
    """A user entry containing entry items."""
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title


class TagCategory(models.TextChoices):
    DATES = 'dates', 'Dates'
    EVENTS = 'events', 'Events'
    PEOPLE = 'people', 'People'
    PLACES = 'places', 'Places'
    THEMES = 'themes', 'Themes'
    TOPICS = 'topics', 'Topics'


class Tag(models.Model):
    """A tag which can be associated to a user entry."""
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=TagCategory.choices)
    entries = models.ManyToManyField(Entry, related_name='tags')
    entry_count = models.PositiveIntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(PolymorphicModel):
    """A base mode for entry items."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='items',
    )

    class Meta:
        unique_together = ('entry', 'title')
        ordering = ['order', 'date_added']

    def __str__(self):
        return self.title
    
    @property
    def item_type(self):
        return getattr(self, 'type_key', self.__class__.__name__.lower())
    

class Paragraph(Item):
    """A plain paragraph."""
    type_key = 'paragraph'
    body = models.TextField()


class Quotation(Item):
    """A quotation."""
    type_key = 'quotation'
    body = models.TextField()
    author = models.CharField(max_length=200, blank=True)


class Letter(Item):
    """A letter."""
    type_key = 'letter'
    date = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    salutation = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    closing = models.CharField(max_length=200, blank=True)
    signature = models.CharField(max_length=200, blank=True)
    postscript = models.TextField(blank=True)


class Recipe(Item):
    """A recipe."""
    type_key = 'recipe'
    time = models.CharField(max_length=100, blank=True)
    servings = models.CharField(max_length=50, blank=True)
    ingredients = models.TextField(help_text="Only one ingredient per line!")
    directions = models.TextField()


class Technical(Item):
    """A technical document."""
    type_key = 'technical'
    body = models.TextField(
        help_text="Enter LaTeX display math without any newline characters.",
    )


class ItemType(models.TextChoices):
    PARAGRAPH = Paragraph.type_key, 'Paragraph'
    QUOTATION = Quotation.type_key, 'Quotation'
    LETTER = Letter.type_key, 'Letter'
    RECIPE = Recipe.type_key, 'Recipe'
    TECHNICAL = Technical.type_key, 'Technical Document'