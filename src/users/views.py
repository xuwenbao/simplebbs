# coding: utf-8
from utils.views import MongoCreateView as CreateView
from utils.views import MongoUpdateView as UpdateView
from .models import User
from .forms import UserForm


class UserCreateView(CreateView):
    
    model = User
    form_class = UserForm

    def form_valid(self, form):
        self.object = form.save()
        return super(UserCreateView, self).form_valid(form)
