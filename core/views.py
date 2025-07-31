from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import EntryForm, ItemTypeForm, TagForm, ITEM_FORMS
from .models import Entry, Item, ItemType, Tag, TagCategory


def index(request):
    """The home page for CommonPlace."""
    if request.user.is_authenticated:
        entries = (
            Entry.objects
            .filter(owner=request.user)
            .order_by('-date_added')
            .values('id', 'title', 'date_added')
        )
        context = {'entries': entries, 'count': entries.count()}       
        return render(request, 'core/index.html', context)
    
    context = {
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm(),
    }   
    return render(request, 'core/welcome.html', context)


@login_required
def category(request, slug):
    """Show a single category and all associated tags."""
    if slug not in TagCategory.values:
        raise Http404("Category does not exist")

    tags = (
        Tag.objects
        .filter(category=slug, owner=request.user)
        .order_by('name')
        .values('id', 'name')
    )
    context = {
        'category': TagCategory(slug).label,
        'tags': tags,
        'count': tags.count(),
    }
    return render(request, 'core/category.html', context)


@login_required
def tag(request, tag_id):
    """Show a single tag and all associated entries."""
    tag = get_object_or_404(Tag, id=tag_id, owner=request.user)
    entries = (
        tag.entries
        .order_by('title')
        .values('id', 'title', 'date_added')
    )
    context = {
        'tag': tag.name,
        'entries': entries,
        'count': entries.count(),
    }
    return render(request, 'core/tag.html', context)


@login_required
def search_tag(request):
    """Search for an existing tag."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)

    tags = (
        Tag.objects
        .filter(owner=request.user, name__icontains=query)
        .values('id', 'name')[:10]
    )
    results = [{'id': t['id'], 'name': t['name']} for t in tags]
    return JsonResponse(results, safe=False)


@login_required
def entry(request, entry_id):
    """Show a single entry and all associated data."""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    tags = entry.tags.order_by('name').values('id', 'name')
    items = entry.items.all()

    context = {
        'entry': entry,
        'tags': tags,
        'tag_count': tags.count(),
        'items': items,
        'item_count': items.count(),
        'edit_entry_form': EntryForm(instance=entry),
        'create_tag_form': TagForm(),
        'select_item_form': ItemTypeForm(),
    }
    return render(request, 'core/entry.html', context)


@login_required
def search_entry(request):
    """Search for an existing entry."""
    query = request.GET.get('q', '').strip()    
    if not query:
        return JsonResponse([], safe=False)

    entries = (
        Entry.objects
        .filter(owner=request.user, title__icontains=query)
        .values('id', 'title')[:10]
    )
    results = [{'id': e['id'], 'name': e['title']} for e in entries]
    return JsonResponse(results, safe=False)


@login_required
@require_POST
def create_entry(request):
    """Create a new entry."""
    form = EntryForm(data=request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.owner = request.user
        entry.save()
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('core:entry', args=[entry.id]),
        })
    
    html = render_to_string(
        'core/partials/create_entry_form.html',
        {'create_entry_form': form},
        request=request,
    )
    return JsonResponse({'success': False, 'form_html': html})


@login_required
@require_POST
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    form = EntryForm(instance=entry, data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('core:entry', args=[entry_id]),
        })
    
    html = render_to_string(
        'core/partials/edit_entry_form.html',
        {'edit_entry_form': form},
        request=request,
    )
    return JsonResponse({'success': False, 'form_html': html})


@login_required
@require_POST
def delete_entry(request, entry_id):
    """Delete an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    entry.tags.update(entry_count=F('entry_count') - 1)
    entry.tags.filter(entry_count=0).delete()
    entry.delete()
    return redirect('core:index')


@require_POST
@login_required
def add_tag(request, entry_id):
    """Add an existing tag to an existing entry."""
    tag_id = request.POST.get('tag_id')
    if not tag_id or not tag_id.isdigit():
        return redirect('core:entry', entry_id)

    tag = get_object_or_404(Tag, id=tag_id, owner=request.user)
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    if not entry.tags.filter(id=tag_id).exists():
        tag.entry_count += 1
        tag.save()
        entry.tags.add(tag)

    return redirect('core:entry', entry_id)


@login_required
@require_POST
def create_tag(request, entry_id):
    """Create a new tag for an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    form = TagForm(data=request.POST)
    if form.is_valid():
        tag = form.save(commit=False)
        tag.owner = request.user
        tag.save()
        entry.tags.add(tag)
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('core:entry', args=[entry_id]),
        })
    
    html = render_to_string(
        'core/partials/create_tag_form.html',
        {'create_tag_form': form},
        request=request,
    )
    return JsonResponse({'success': False, 'form_html': html})


@login_required
@require_POST
def remove_tag(request, entry_id, tag_id):
    """Remove a tag associated to an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    tag = get_object_or_404(entry.tags, id=tag_id)
    entry.tags.remove(tag)
    tag.entry_count -= 1
    if tag.entry_count == 0:
        tag.delete()
    else:
        tag.save()
    return redirect('core:entry', entry_id=entry_id)


@login_required
@require_POST
def select_item(request, entry_id):
    """Select the type of entry item to create."""
    form = ItemTypeForm(data=request.POST)
    if form.is_valid():
        item_type = form.cleaned_data['item_type']
        return JsonResponse({
            'success': True,
            'redirect_url': reverse(
                'core:create_item',
                args=[entry_id, item_type],
            ),
        })

    html = render_to_string(
        'core/partials/select_item_form.html',
        {'select_item_form': form},
        request=request,
    )
    return JsonResponse({'success': False, 'form_html': html})


@login_required
def create_item(request, entry_id, item_type):
    """Create a new item of the given type."""
    entry = get_object_or_404(Entry, id=entry_id, owner=request.user)
    if request.method != 'POST':
        form = ITEM_FORMS[item_type]()
    else:
        form = ITEM_FORMS[item_type](data=request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.entry = entry
            item.save()
            return redirect('core:entry', entry_id=entry_id)
        
    context = {
        'entry_id': entry.id,
        'item_type': item_type,
        'item_label': ItemType(item_type).label,
        'create_item_form': form,
    }
    return render(request, 'core/create_item.html', context)


@login_required
def edit_item(request, item_id):
    """Edit an existing item."""
    item = get_object_or_404(Item, id=item_id)
    if item.entry.owner != request.user:
        raise Http404
    
    item_type = item.type_key
    if request.method != 'POST':
        form = ITEM_FORMS[item_type](instance=item)
    else:
        form = ITEM_FORMS[item_type](instance=item, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:entry', entry_id=item.entry.id)
        
    context = {
        'item_id': item.id,
        'entry_id': item.entry.id,
        'item_label': ItemType(item_type).label,
        'edit_item_form': form,
    }
    return render(request, 'core/edit_item.html', context)


@login_required
@require_POST
def delete_item(request, item_id):
    """Delete an existing item."""
    item = get_object_or_404(Item, id=item_id)
    if item.entry.owner != request.user:
        raise Http404
    
    entry_id = item.entry.id
    item.delete()
    return redirect('core:entry', entry_id=entry_id)