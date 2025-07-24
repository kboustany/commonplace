from django.db import models
from django.contrib.auth.models import User

from polymorphic.models import PolymorphicModel


class Category(models.Model):
    """A general category for storing tags."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    """A tag which can be associated to a user entry."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    entry_count = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='tags',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Entry(models.Model):
    """An entry to be made by the user containing items and tags."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='entries',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.name
    

class ItemBase(PolymorphicModel):
    """A base class for an item contained in an entry."""
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    gpt_entry = models.TextField(null=True)
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='items',
    )

    def __str__(self):
        return self.name
    
    def get_prompt(self):
        """Return a custom prompt about this item for ChatGPT."""
        pass

    
class PlainItem(ItemBase):
    """An unformatted plain text item."""
    item_type = models.CharField(
        max_length=20,
        default='plain',
    )
    body = models.TextField()

    def get_prompt(self):
        """Return a custom prompt about this item for ChatGPT."""
        tag_names = ', '.join([tag.name for tag in self.entry.tags.all()])
        prompt = f"""In at most one paragraph, comment on the paragraph
        {self.body}, using the following context:
        It is titled: {self.name}.
        It is part of a larger entry titled: {self.entry.name}.
        That entry is tagged with the following tags:
        {tag_names}.
        Prioritize making sure there are no incorrect statements;
        otherwise give further information. Do not mention external elements
        such as entries or tags in your response."""
        return prompt

  
# Letter, Recipe, Quotation, Image