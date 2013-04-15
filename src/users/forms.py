# coding: utf-8
import re

from django import forms


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

        m = re.match('[a-zA-Z0-9]+', username)
        if not m:
            raise forms.ValidationError, u'请使用半角的 a-z 或数字 0-9'
        return username