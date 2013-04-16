# coding: utf-8
import re

from django import forms

from .models import User


class UserForm(forms.Form):

    username = forms.CharField(max_length=30, required=True, label=u'用户名',
        help_text=u'请使用半角的 a-z 或数字 0-9')
    password = forms.CharField(min_length=6, max_length=30, required=True, label=u'密码',
        help_text=u'请输入6至30位密码', widget=forms.PasswordInput)
    email = forms.EmailField(required=True, label=u'电子邮件',
        help_text=u'请使用真实电子邮箱注册')
    # avatar = forms.ImageField(label=u'头像')

    def clean_username(self):
        username = self.cleaned_data['username']

        # 用户名必须为字母或数字
        m = re.match('[a-zA-Z0-9]+', username)
        if not m:
            raise forms.ValidationError, u'请使用半角的 a-z 或数字 0-9'

        # 用户名不能重复
        if User.is_username_exist(username):
            raise forms.ValidationError, u'用户名已存在'
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        # email不能重复
        if User.is_email_exist(email):
            raise forms.ValidationError, u'该电子邮箱已注册'
        return email