# coding: utf-8
from braces.views import JSONResponseMixin, CsrfExemptMixin

from utils.mixins import UserMixin
from utils.views import MongoCreateView as CreateView
from utils.views import MongoListView as ListView
from utils.security import (
    login, 
    logout,
    permission_view,
    Allow,
    EveryOne,
    Owner,
    Authenticated,
)

from users.models import User
from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostListView(UserMixin, ListView):
    """
    Post列表
    """

    model = Post
    paginate_by = 5

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


class CommentListView(UserMixin, ListView):
    """
    显示Post,与comment列表.
    """

    model = Comment
    paginate_by = 5

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        self.post = Post.objects.get(id=post_id)
        return self.post.comments

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        context.update({'post': self.post})
        return context

    def get_template_names(self):
        if self.kwargs.get('render_type') == 'include':
            return ['_comment_pagination.html']
        else:
            return ['comment_list.html']


class CommentCreateView(JSONResponseMixin, CreateView):
    """
    创建Comment.返回成功或失败的json数据
    """

    model = Comment
    form_class = CommentForm

    def form_invalid(self, form):
        context = {
            'status': 'fail',
        }
        return self.render_json_response(context)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        post_id = form.cleaned_data['post_id']
        content = form.cleaned_data['content']

        Comment.create_comment(post_id, username, content)
        context = {
            'status': 'success',
        }
        return self.render_json_response(context)


post_list = permission_view(PostListView.as_view(), permission='view', model=Post)
post_create = permission_view(PostCreateView.as_view(), permission='add', model=Post)
comment_list = permission_view(CommentListView.as_view(), permission='view', model=Comment)
comment_create = permission_view(CommentCreateView.as_view(), permission='add', model=Comment)
