from django.urls import path

from . import views


app_name = 'core'

urlpatterns = [
    # Landing page for CommonPlace.
    path(
        route='',
        view=views.index,
        name='index',
    ),
    # Detail page for a single category.
    path(
        route='categories/<slug:slug>/',
        view=views.category,
        name='category',
    ),
    # Detail page for a single tag.
    path(
        route='tags/<int:tag_id>/',
        view=views.tag,
        name='tag',
    ),
    # Form for searching for a tag.
    path(
        route='tags/search/',
        view=views.search_tag,
        name='search_tag',
    ),
    # Detail page for a single entry.
    path(
        route='entries/<int:entry_id>/',
        view=views.entry,
        name='entry',
    ),
    # Form for searching for an entry.
    path(
        route='entries/search/',
        view=views.search_entry,
        name='search_entry',
    ),
    # Form for creating a new entry.
    path(
        route='create_entry/',
        view=views.create_entry,
        name='create_entry',
    ),
    # Form for editing an entry.
    path(
        route='edit_entry/<int:entry_id>/',
        view=views.edit_entry,
        name='edit_entry',
    ),
    # Modal for deleting an entry.
    path(
        route='delete_entry/<int:entry_id>/',
        view=views.delete_entry,
        name='delete_entry'
    ),
    # Modal for adding an existing tag.
    path(
        route='add_tag/<int:entry_id>/',
        view=views.add_tag,
        name='add_tag',
    ),
    # Form for creating a new tag.
    path(
        route='create_tag/<int:entry_id>/',
        view=views.create_tag,
        name='create_tag',
    ),
    # Modal for removing a tag.
    path(
        route='remove_tag/<int:entry_id>/<int:tag_id>/',
        view=views.remove_tag,
        name='remove_tag',
    ),
]