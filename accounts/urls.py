from django.urls import path, include

from . import views


app_name = 'accounts'
urlpatterns = [
    # Include default authentication URLs.
    path(
        route='',
        view=include('django.contrib.auth.urls'),
    ),
    # Registration page.
    path(
        route='register/',
        view=views.register,
        name='register',
    ),
]