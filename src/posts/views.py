# coding: utf-8
from braces.views import JSONResponseMixin, CsrfExemptMixin

from utils.mixins import UserMixin
from utils.views import MongoCreateView as CreateView
from utils.views import MongoListView as ListView

from .models import Post
from .forms import PostForm


class PostListView(UserMixin, ListView):
    """
    Post列表
    """

    model = Post
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by('-create_time')

    def get_template_names(self):
        if self.kwargs.get('render_type') == 'include':
            return ['_post_pagination.html']
        else:
            return ['post_list.html']


class PostCreateView(JSONResponseMixin, CreateView):
    """
    创建Post.返回成功或失败的json数据.
    """

    model = Post
    form_class = PostForm

    def form_invalid(self, form):
        context = {
            'status': 'fail',
        }
        return self.render_json_response(context)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        Post.create_post(username, title, content)
        context = {
            'status': 'success',
        }
        return self.render_json_response(context)


post_list = PostListView.as_view()