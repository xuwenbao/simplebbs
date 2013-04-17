from django.conf.urls import patterns, include, url

from .views import (
    PostListView,
    PostCreateView,
) 

urlpatterns = patterns('',
    url(r'^create/$', PostCreateView.as_view(), name='post.create'),
    url(r'^list/include/$', PostListView.as_view(), {'render_type': 'include'}, name='post.list_incldue'),
)