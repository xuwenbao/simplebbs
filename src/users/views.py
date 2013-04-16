# coding: utf-8
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse, reverse_lazy

from utils.security import login, logout
from utils.views import MongoCreateView as CreateView
from utils.views import MongoUpdateView as UpdateView
from utils.views import MongoDetailView as DetailView
from .models import User, RestToken
from .forms import UserForm


class UserCreateView(CreateView):
    """
    创建用户
    """
    
    model = User
    form_class = UserForm
    success_url = reverse_lazy('post.list')

    def form_valid(self, form):
        self.object = user = User.create_user(username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'])
        login(self.request, user.username)
        messages.success(self.request, u'注册成功.')
        return super(UserCreateView, self).form_valid(form)


class LoginView(TemplateView):
    """
    登录页面
    """
    template_name = 'user_login.html'


class LoginRedirectView(RedirectView):
    """
    登录验证,跳转
    """

    def post(self, request, *args, **kwargs):
        username = self.request.POST['username']
        password = self.request.POST['password']
        if User.check_password(username, password):
            login(request, username)
            self.url = reverse('post.list')
            messages.success(request, u'登录成功')
        else:
            messages.error(request, u'用户名或密码错误')
            self.url = reverse('user.login')
        return super(LoginRedirectView, self).post(request, *args, **kwargs)


class LogoutRedirectView(RedirectView):
    """
    登出
    """

    url = reverse_lazy('post.list')

    def post(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutRedirectView, self).post(request, *args, **kwargs)


class ForgetPwdView(TemplateView):
    """
    找回密码页面
    """
    template_name = 'user_findpwd.html'

    def get_context_data(self, **kwargs):
        context = super(ForgetPwdView, self).get_context_data(**kwargs)
        context.update({
            'username': self.request.GET.get('username', ''),
            'email': self.request.GET.get('email', ''),
        })
        return context


mail_message = """Hi {username},

我们的系统收到一个请求，说你希望通过电子邮件重新设置你在 V2EX 的密码。你可以点击下面的链接开始重设密码：

{reset_uri}

如果这个请求不是由你发起的，那没问题，你不用担心，你可以安全地忽略这封邮件。此链接会在两天后自动失效.

此页面访问一次后就会失效.

如果你有任何疑问，可以回复这封邮件向我们提问.
"""


class ForgetPwdRedirectView(RedirectView):
    """
    找回密码校验,发送找回密码邮件
    """

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']

        self.url = '{0}?username={1}&email={2}'.format(reverse('user.findpwd'), username, email)
        if not User.check_email(username, email):
            messages.error(request, u'用户名或电子邮件不正确')
        else:
            # 发送找回密码邮件.
            token = RestToken.create_resttoken(username)
            reset_uri = request.build_absolute_uri(reverse('user.resetpwd', kwargs={'slug': token.reset_token}))
            message = mail_message.format(username=username, reset_uri=reset_uri)
            User.mail_to_user(username, email, u'[Simplebbs]重设密码', message)
            messages.success(request, u'邮件已发送,请查看邮箱(邮件可能会存在几分钟的延迟).')

        return super(ForgetPwdRedirectView, self).post(request, *args, **kwargs)


class RestPwdView(DetailView):
    """
    重新设置密码
    """

    model = RestToken
    slug_field = 'reset_token'

    def get_queryset(self):
        """
        过滤已过期和访问过的Token
        """
        return RestToken.objects.filter(expire_time__gt=timezone.now(), used=False)

    def get_object(self, queryset=None):
        """
        访问的Token立即标记为已使用
        """
        obj = super(RestPwdView, self).get_object(queryset)
        obj.use()
        return obj
