from django.conf.urls import patterns, include, url

from .views import PostListView

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='post.list'),
)