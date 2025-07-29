from django.contrib.auth.models import User
from django.db import models


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
    entry_count = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name