from django.utils import timezone
from mongoengine import (
    Document,
    EmbeddedDocument,
    IntField,
    ListField,
    StringField,
    DateTimeField,
    ReferenceField,
    EmbeddedDocumentField,
    CASCADE,
)


class Comment(EmbeddedDocument):

    author = ReferenceField('users.User')
    content = StringField(max_length=500, required=True)
    create_time = DateTimeField(default=timezone.now())

    meta = {
        'ordering': ['create_time'],
        'app_label': 'users',
        'object_name': 'User',
    }


class Post(Document):

    author = ReferenceField('users.User', reverse_delete_rule=CASCADE)
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=1024, required=True)
    tags = ListField(StringField(max_length=50))
    comments = ListField(EmbeddedDocumentField(Comment))
    page_views = IntField(default=0)
    create_time = DateTimeField(default=timezone.now())

    meta = {
        'ordering': ['-create_time'],
        'app_label': 'users',
        'object_name': 'User',
    }
