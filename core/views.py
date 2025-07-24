from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import (
    Category,
    Tag,
    Entry,
    ItemBase,
)
from .forms import (
    EntryForm,
    TagForm,
    PlainForm,
)
from .gpt import get_tag_description, get_item_comment


FORMS = {
    'plain': PlainForm,
}


def index(request):
    """The home page for CommonPlace."""
    return render(request, 'core/index.html')

@login_required
def category(request, slug):
    """Show a single category and all associated tags."""
    category = Category.objects.get(slug=slug)
    tags = category.tags.filter(owner=request.user).order_by('name')
    context = {
        'category': category,
        'tags': tags,
    }
    return render(request, 'core/category.html', context)

@login_required
def tag(request, tag_id):
    """Show a single tag and all associated entries."""
    tag = Tag.objects.get(id=tag_id)
    check_owner(tag, request.user)
    entries = tag.entries.order_by('name')
    context = {
        'tag': tag,
        'entries': entries,
    }
    return render(request, 'core/tag.html', context)

@login_required
def entries(request):
    """Show all entries."""
    entries = Entry.objects.filter(owner=request.user).order_by('date_added')
    context = {
        'entries': entries,
    }
    return render(request, 'core/entries.html', context)

@login_required
def entry(request, entry_id):
    """Show a single entry and all enclosed items."""
    entry = Entry.objects.get(id=entry_id)
    check_owner(entry, request.user)
    tags = entry.tags.order_by('name')
    items = entry.items.order_by('-date_added')
    all_tags = Tag.objects.filter(owner=request.user).order_by('name')
    context = {
        'entry': entry,
        'tags': tags,
        'items': items,
        'all_tags': all_tags,
        'item_types': FORMS.keys(),
    }
    return render(request, 'core/entry.html', context)

@login_required
def create_entry(request):
    """Create a new entry."""
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = request.user
            entry.save()
            return redirect('core:entry', entry_id=entry.id)
    
    context = {
        'form': form,
    }
    return render(request, 'core/create_entry.html', context)

@login_required
@require_POST
def delete_entry(request, entry_id):
    """Delete an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    check_owner(entry, request.user)
    entry.tags.update(entry_count=F('entry_count') - 1)
    orphans = entry.tags.filter(entry_count=0)
    orphans.delete()
    entry.delete()
    return redirect('core:entries')

@login_required
def add_tag(request, entry_id, tag_id):
    """Associate an existing tag to an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    check_owner(entry, request.user)
    tag = get_object_or_404(Tag, id=tag_id)
    if tag not in entry.tags.all():
        tag.entry_count += 1
        tag.save()
        entry.tags.add(tag)
    return redirect('core:entry', entry_id=entry_id)

@login_required
def create_tag(request, entry_id):
    """Associate a new tag to an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    check_owner(entry, request.user)
    if request.method != 'POST':
        form = TagForm()
    else:
        form = TagForm(data=request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.description = get_tag_description(tag.name, tag.category)
            tag.entry_count += 1
            tag.owner = request.user
            tag.save()
            entry.tags.add(tag)
            return redirect('core:entry', entry_id=entry_id)
    
    context = {
        'form': form,
        'entry': entry,
    }
    return render(request, 'core/create_tag.html', context)

@login_required
@require_POST
def remove_tag(request, entry_id, tag_id):
    """Remove a tag associated to an entry."""
    entry = Entry.objects.get(id=entry_id)
    check_owner(entry, request.user)
    tag = Tag.objects.get(id=tag_id)
    entry.tags.remove(tag)
    tag.entry_count -= 1
    tag.save()
    if tag.entry_count == 0:
        tag.delete()
    return redirect('core:entry', entry_id=entry_id)

@login_required
def create_item(request, item_type, entry_id):
    """Create an item in an entry."""
    if item_type not in FORMS.keys():
        raise Http404("Item type is not valid.")
    entry = Entry.objects.get(id=entry_id)
    check_owner(entry, request.user)
    if request.method != 'POST':
        form = FORMS[item_type]
    else:
        form = FORMS[item_type](data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.entry = entry
            item.item_type = item_type
            item.save()
            return redirect('core:entry', entry_id=entry_id)
    
    context = {
        'form': form,
        'entry': entry,
        'item_type': item_type,
    }
    return render(request, 'core/create_item.html', context)

@login_required
def edit_item(request, item_id):
    """Edit an existing item."""
    item = ItemBase.objects.get(id=item_id)
    item_type = item.item_type
    entry = item.entry
    check_owner(entry, request.user)
    if request.method != 'POST':
        form = FORMS[item_type](instance=item)
    else:
        form = FORMS[item_type](instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:entry', entry_id=entry.id)
        
    context = {
        'form': form,
        'item': item,
        'entry': entry,
    }
    return render(request, 'core/edit_item.html', context)

@login_required
@require_POST
def delete_item(request, item_id):
    """Delete an existing item."""
    item = ItemBase.objects.get(id=item_id)
    entry = item.entry
    check_owner(entry, request.user)
    item.delete()
    return redirect('core:entry', entry_id=entry.id)

@login_required
def get_comment(request, item_id):
    """Obtain and display ChatGPT's comment on an existing item."""
    item = ItemBase.objects.get(id=item_id)
    check_owner(item.entry, request.user)
    flag = request.GET.get("flag", "false")
    refresh = (flag.lower() == "true")
    if (item.gpt_entry is None) or refresh is True:
        item.gpt_entry = get_item_comment(item.get_prompt())
        item.save()
    context = {
        'item': item,
    }
    return render(request, 'core/get_comment.html', context)

# Utilities

def check_owner(model, user):
    if model.owner != user:
        raise Http404