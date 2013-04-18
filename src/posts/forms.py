# coding: utf-8
from django import forms


class PostForm(forms.Form):

    username = forms.CharField(required=True)
    title = forms.CharField(required=True, min_length=1, max_length=120)
    content = forms.CharField(required=True, min_length=1, max_length=1024)


class CommentForm(forms.Form):

    post_id = forms.CharField(required=True)
    username = forms.CharField(required=True)
    content = forms.CharField(required=True, min_length=1, max_length=1024)
