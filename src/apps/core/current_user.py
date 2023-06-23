from threading import local

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')

_thread_locals = local()


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME, user_fun.__get__(user_fun, local))


def _set_current_user(user=None):
    """
    Sets current user in local thread.
    Can be used as a hook, e.g., for shell jobs (when the request object is
    not available).
    """
    _do_set_current_user(lambda self: user)


class SetCurrentUser:
    def __init__(self, request):
        self.request = request

    def __enter__(self):
        _do_set_current_user(lambda this: getattr(self.request, 'user', None))

    def __exit__(self, user_type, value, traceback):
        _do_set_current_user(lambda this: None)


class ThreadLocalUserMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.user closure; asserts laziness;
        # memorization is implemented in
        # request.user (non-data descriptor)
        with SetCurrentUser(request):
            response = self.get_response(request)
        return response


def get_current_user():
    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
    if callable(current_user):
        return current_user()
    return current_user


def get_current_authenticated_user():
    current_user = get_current_user()
    if isinstance(current_user, AnonymousUser):
        return None
    return current_user
