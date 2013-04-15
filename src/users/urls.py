from django.conf.urls import patterns, include, url

from .views import UserCreateView

urlpatterns = patterns('',
    url(r'^create/$', UserCreateView.as_view(), name='user.create'),
)