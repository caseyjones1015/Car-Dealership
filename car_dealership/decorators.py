# decorators.py
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.http import HttpResponse


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Your logic to check if the user is an admin
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        else:
            # Redirect or handle unauthorized access here
            # Example: Redirect to login or show an error page
            return HttpResponse("Unauthorized access", status=401)
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Your logic to check if the user is an admin
        if request.user.is_authenticated and request.user.role.role == 'admin':
            return view_func(request, *args, **kwargs)

        elif request.user.is_authenticated and request.user.role.role == 'moderator':
            return view_func(request, *args, **kwargs)

        else:
            # Redirect or handle unauthorized access here
            # Example: Redirect to login or show an error page
            return HttpResponse("Unauthorized access", status=401)
    return _wrapped_view
