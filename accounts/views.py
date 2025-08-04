from django.contrib.auth import login as django_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse


def login(request):
    """Log in to an existing user."""
    if request.method != 'POST':
        return redirect('core:index')

    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        django_login(request, form.get_user())
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('core:index'),
        })

    html = render_to_string(
        'core/partials/login_form.html',
        {'login_form': form},
        request=request,
    )
    return JsonResponse({'success': False, 'form_html': html})


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        return redirect('core:index')
    
    form = UserCreationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        django_login(request, user)
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('core:index'),
        })
    
    html = render_to_string(
        'core/partials/register_form.html',
        {'register_form': form},
        request=request,
    )
    return JsonResponse({'success': False, 'form_html': html})