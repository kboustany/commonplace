from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    # Home page.
    path(
        route='',
        view=views.index,
        name='index'
    ),
    # Detail page for a single category.
    path(
        route='categories/<slug:slug>/',
        view=views.category,
        name='category'
    ),
    # Detail page for a single tag.
    path(
        route='tags/<int:tag_id>/',
        view=views.tag,
        name='tag'
    ),
    # Detail page for all entries.
    path(
        route='entries/',
        view=views.entries,
        name='entries'
    ),
    # Detail page for a single entry.
    path(
        route='entries/<int:entry_id>/',
        view=views.entry,
        name='entry'
    ),
    # Page for creating a new entry.
    path(
        route='create_entry/',
        view=views.create_entry,
        name='create_entry'
    ),
    # Page for deleting an entry.
    path(
        route='delete_entry/<int:entry_id>/',
        view=views.delete_entry,
        name='delete_entry'
    ),
    # Page for adding an existing tag.
    path(
        route='add_tag/<int:entry_id>/<int:tag_id>/',
        view=views.add_tag,
        name='add_tag'
    ),
    # Page for creating a new tag.
    path(
        route='create_tag/<int:entry_id>/',
        view=views.create_tag,
        name='create_tag'
    ),
    # Page for removing a tag from an entry.
    path(
        route='remove_tag/<int:entry_id>/<int:tag_id>/',
        view=views.remove_tag,
        name='remove_tag'
    ),
    # Page for creating a new item in an entry.
    path(
        route='create_item/<str:item_type>/<int:entry_id>/',
        view=views.create_item,
        name='create_item'
    ),
    # Page for editing an existing item in an entry.
    path(
        route='edit_item/<int:item_id>/',
        view=views.edit_item,
        name='edit_item'
    ),
    # Page for deleting an item in an entry.
    path(
        route='delete_item/<int:item_id>/',
        view=views.delete_item,
        name='delete_item'
    ),
    # Page for displaying a ChatGPT comment about an item.
    path(
        route='get_comment/<int:item_id>/',
        view = views.get_comment,
        name='get_comment'
    ),
]