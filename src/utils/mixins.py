# coding: utf-8


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