from django.views.generic import TemplateView

from utils.mixins import UserMixin


class PostListView(UserMixin, TemplateView):
    template_name = 'index.html'
