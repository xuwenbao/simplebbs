# coding: utf-8
from django.conf import settings


class Allow(object):
    
    @classmethod
    def validate(cls, group, user_groups, model=None, instance=None, username=None):
        if isinstance(group, basestring):
            return group in user_groups
        return group.validate(group, user_groups, model=model, instance=instance, username=username)


class Deny(object):
    pass


class EveryOne(object):
    
    @classmethod
    def validate(cls, group, user_groups, model=None, instance=None, username=None):
        return True


class Owner(object):
    
    @classmethod
    def validate(cls, group, user_groups, model=None, instance=None, username=None):
        return instance.is_owner(username)


class Authenticated(object):

    @classmethod
    def validate(cls, group, user_groups, model=None, instance=None, username=None):
        if username:
            return True
        return False


def permission_view(view, permission, model, slug=None, slug_kwarg=None):
    """
    view视图的权限装饰器
    """
    def wrapper(*args, **kwargs):
        return view(*args, **kwargs)
        
    wrapper.permission = permission
    wrapper.permission_model = model
    wrapper.permission_slug = slug
    wrapper.permission_slug_kwarg = slug_kwarg
    return wrapper


def has_permission(permission, user_groups, model=None, instance=None, username=None):
    if (not hasattr(model, '__acl__')) and (not hasattr(instance, '__acl__')):
        return True

    if hasattr(model, '__acl__'):
        acl = model.__acl__
    else:
        acl = instance.__acl__
        
    opeator, group, perm = filter(lambda l: l[2] == permission, acl)[0]
    return opeator.validate(group, user_groups, model=model, instance=instance, username=username)


def login(request, username):
    request.session['username'] = username


def logout(request):
    request.session['username'] = ''