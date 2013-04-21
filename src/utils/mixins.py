# coding: utf-8
from utils.security import has_permission

class UserMixin(object):
    """
    在context中加入username变量.
    已登录用户为该用户的username,未登录时为None.
    """
    def get_context_data(self, **kwargs):
        context = super(UserMixin, self).get_context_data(**kwargs)
        username = self.request.session.get('username')
        context.update({'username': username})
        return context


class PermissionMixin(object):
    """
    Model PermissionMixin
    """
    def has_perm(self, permission, user_groups, username):
        return has_permission(permission, user_groups=user_groups, instance=self, username=username)

    def is_owner(self, username):
        raise NotImplementedError