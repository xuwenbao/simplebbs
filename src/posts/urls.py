from django.conf.urls import patterns, include, url

urlpatterns = patterns('posts.views',
    url(r'^create/$', 'post_create', name='post.create'),
    url(r'^delete/(?P<post_id>\w+)/$', 'post_delete', name='post.delete'),
    url(r'^list/include/$', 'post_list', {'render_type': 'include'}, name='post.list_incldue'),
    url(r'^detail/(?P<post_id>\w+)/$', 'comment_list', name='comment.list'),
    url(r'^detail/(?P<post_id>\w+)/include/$', 'comment_list', {'render_type': 'include'}, name='comment.list_include'),
    url(r'^comment/create/$', 'comment_create', name='comment.create'),
)