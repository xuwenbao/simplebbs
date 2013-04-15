from django.utils import timezone
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
        (Allow, EveryOne, 'add'),
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
        return cls(username=username, password=password, email=email)
