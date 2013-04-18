# coding: utf-8
from django.http import HttpResponseForbidden

from utils.security import has_permission
from .models import groupfinder

class PermissionMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'permission'):
            username = request.session.get('username')
            user_groups = groupfinder(request)
            permission = view_func.permission
            model = view_func.permission_model
            slug = view_func.permission_slug
            slug_kwarg = view_func.permission_slug_kwarg
            if slug and slug_kwarg:
                value = view_kwargs.get(slug_kwarg)
                if value:
                    instance = model.objects.get(**{slug: value})
            else:
                instance = None

            if not has_permission(permission, user_groups, model, instance, username):
                return HttpResponseForbidden()
