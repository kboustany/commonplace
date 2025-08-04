from .forms import EntryForm
from .models import TagCategory


def context(request):
    """Provides a global context for CommonPlace."""
    context = {
        'create_entry_form': EntryForm(),
        'categories': TagCategory.choices,
    }
    return context
