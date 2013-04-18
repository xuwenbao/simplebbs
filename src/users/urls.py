from django.conf.urls import patterns, include, url

urlpatterns = patterns('users.views',
    url(r'^create/$', 'create', name='user.create'),
    url(r'^login/$', 'login', name='user.login'),
    url(r'^login/check/$', 'login_check', name='user.login_check'),
    url(r'^logout/$', 'logout', name='user.logout'),
    url(r'^findpwd/$', 'findpwd', name='user.findpwd'),
    url(r'^findpwd/check/$', 'findpwd_check', name='user.findpwd_check'),
    url(r'^reset/check/$', 'resetpwd_check', name='user.resetpwd_check'),
    url(r'^reset/(?P<slug>\w+)/$', 'resetpwd', name='user.resetpwd'),
)