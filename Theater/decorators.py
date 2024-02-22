from functools import wraps

from django.http import HttpResponseForbidden


def position_required(positions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('employee_position') in positions:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("У вас нет доступа к этой странице")

        return _wrapped_view

    return decorator
