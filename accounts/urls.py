from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    # Login page.
    path(
        route='login/',
        view=views.login,
        name='login',
    ),

    # Logout page.
    path(
        route='logout/',
        view=LogoutView.as_view(),
        name='logout',
    ),

    # Registration page.
    path(
        route='register/',
        view=views.register,
        name='register',
    ),
]