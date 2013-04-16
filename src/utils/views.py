# coding: utf-8
"""
此模块的目的是重写Django通用视图的方法,使通用视图支持MongoEngine的Model
"""
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from mongoengine import Document, EmbeddedDocument
from mongoengine.queryset import DoesNotExist

from .mixins import UserMixin


class MongoSingleObjectTemplateResponseMixin(object):
    """
    重写get_template_names方法,沿用通用视图的template_name_suffix属性.
    使用此Mixin的Model必须定义__object_name__.
    如:
    class User(Document):

        __object_name__ = 'Users'
    """
    def get_template_names(self):
        try:
            names = super(MongoSingleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            names = []

        if self.object and self.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            if names:
                names.insert(0, name)

        if isinstance(self.object, (Document, EmbeddedDocument)):
            names.append("%s%s.html" % (
                self.object.__object_name__.lower(),
                self.template_name_suffix
            ))
        elif hasattr(self, 'model') and self.model is not None:
            names.append("%s%s.html" % (
                self.model.__object_name__.lower(),
                self.template_name_suffix
            ))
        return names

    def get_object(self, queryset=None):
        try:
            obj = super(MongoSingleObjectTemplateResponseMixin, self).get_object(queryset)
        except DoesNotExist:
            raise Http404("No record found matching the query")
        else:
            return obj


class MongoFormMixin(object):
    """
    重写涉及form的方法,放弃使用django model form,使用forms.Form.
    使用此Mixin的View必须提供form_class属性和form_valid方法.
    并在form_valid方法中设置object属性.
    """
    def get_form_class(self):
        return self.form_class

    def get_form(self, form_class):
        if self.request.method in ('POST', 'PUT'):
            return form_class(self.request.POST)
        else:
            return form_class()

    def form_valid(self, form):
        if not self.object:
            raise ValueError, 'attr object not setted.'
        return HttpResponseRedirect(self.get_success_url())


class MongoSingleObjectQuerysetMixin(object):
    """
    """
    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model.objects
            else:
                raise ImproperlyConfigured("%(cls)s is missing a queryset. Define "
                                           "%(cls)s.model, %(cls)s.queryset, or override "
                                           "%(cls)s.get_queryset()." % {'cls': self.__class__.__name__}
                                           )
            return self.queryset.clone()


class MongoCreateView(MongoSingleObjectTemplateResponseMixin,
                      MongoFormMixin,
                      MongoSingleObjectQuerysetMixin,
                      CreateView):
    pass


class MongoUpdateView(MongoSingleObjectTemplateResponseMixin,
                      MongoFormMixin,
                      MongoSingleObjectQuerysetMixin,
                      UpdateView):
    pass

 
class MongoDetailView(MongoSingleObjectTemplateResponseMixin,
                       MongoSingleObjectQuerysetMixin,
                       DetailView):

    def get_context_object_name(self, obj):
        """
        Get the name to use for object.
        """
        if self.context_object_name:
            return self.context_object_name
        elif isinstance(obj, (Document, EmbeddedDocument)):
            return obj.__object_name__.lower()
        else:
            return None