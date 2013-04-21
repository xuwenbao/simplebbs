# coding: utf-8
import time
import hashlib
import datetime

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from mongoengine import (
    Document,
    EmbeddedDocument,
    IntField,
    URLField,
    ListField,
    EmailField,
    StringField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocumentField,
    CASCADE,
    OperationError,
)

from utils.security import (
    Allow,
    Deny,
    EveryOne,
    Owner,
    Authenticated,
)


class User(Document):

    username = StringField(max_length=30, required=True, unique=True)
    password = StringField(max_length=100, required=True)
    email = EmailField(required=True, unique=True)
    avatar = URLField()
    groups = ListField(StringField(max_length=30), default=lambda: ['group:user'])
    is_confirm = BooleanField(required=True, default=False)
    is_active = BooleanField(required=True, default=True)
    joined_time = DateTimeField(default=timezone.now())
    last_login = DateTimeField()

    __object_name__ = 'User'
    __acl__ = [
        (Allow, EveryOne, 'commom'),
        (Allow, EveryOne, 'add'),
        (Allow, Authenticated, 'logout'),
        (Allow, Owner, 'change'),
        (Allow, 'group:admin', 'delete'),
    ]

    @classmethod
    def is_owner(cls, request, authenticated_username, slug=None, instance=None):
        if slug:
            return slug == authenticated_username
        if instance:
            return instance.username == authenticated_username
        return False

    @classmethod
    def create_user(cls, username, password, email):
        obj = cls(username=username, password=password, email=email)
        obj.save()
        return obj

    @classmethod
    def get_by_uesrname(cls, username):
        return cls.objects.get(username=username)

    @classmethod
    def check_password(cls, username, password):
        if cls.objects(username=username, password=password).first():
            return True
        return False

    @classmethod
    def change_password(cls, username, password):
        cls.objects(username=username).update_one(set__password=password)

    @classmethod
    def check_email(cls, username, email):
        if cls.objects(username=username, email=email):
            return True
        return False

    @classmethod
    def is_username_exist(cls, username):
        if cls.objects(username=username).first():
            return True
        return False

    @classmethod
    def is_email_exist(cls, email):
        if cls.objects(email=email).first():
            return True
        return False

    @classmethod
    def mail_to_user(cls, username, email, subject, message):
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


class RestToken(Document):

    user = ReferenceField('User', reverse_delete_rule=CASCADE)
    reset_token = StringField(max_length=100, required=True, unique=True)
    used = BooleanField(default=False)
    create_time = DateTimeField(default=timezone.now())
    expire_time = DateTimeField(default=timezone.now() + datetime.timedelta(days=2))

    __object_name__ = 'RestToken'

    @classmethod
    def create_resttoken(cls, username):
        user = User.get_by_uesrname(username)
        # 用email和当前时间戳生成token
        token = hashlib.md5('%s%s' % (user.email, int(time.time()))).hexdigest()
        obj = cls(user=user, reset_token=token)
        obj.save()
        return obj

    def use(self):
        if not self.used:
            self.used = True
            self.save()


def groupfinder(request):
    username = request.session.get('username')
    if not username:
        return []
    return User.get_by_uesrname(username).groups