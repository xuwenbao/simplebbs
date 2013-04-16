from django.conf.urls import patterns, include, url

from .views import (
    UserCreateView,
    LoginView,
    LoginRedirectView,
    LogoutRedirectView,
    ForgetPwdView,
    ForgetPwdRedirectView,
    RestPwdView,
)

urlpatterns = patterns('',
    url(r'^create/$', UserCreateView.as_view(), name='user.create'),
    url(r'^login/$', LoginView.as_view(), name='user.login'),
    url(r'^login/check/$', LoginRedirectView.as_view(), name='user.login_check'),
    url(r'^logout/$', LogoutRedirectView.as_view(), name='user.logout'),
    url(r'^findpwd/$', ForgetPwdView.as_view(), name='user.findpwd'),
    url(r'^findpwd/check/$', ForgetPwdRedirectView.as_view(), name='user.findpwd_check'),
    url(r'^reset/(?P<slug>\w+)/$', RestPwdView.as_view(), name='user.resetpwd'),
)