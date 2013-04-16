from django.conf import settings


class Allow(object):
    pass


class Deny(object):
    pass


class EveryOne(object):
    pass


class Owner(object):
    pass


class Authenticated(object):
    pass


def has_permission():
    pass


def login(request, username):
    request.session['username'] = username


def logout(request):
    request.session['username'] = ''