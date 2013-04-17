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

from users.models import User

class Comment(EmbeddedDocument):

    author = ReferenceField('users.User')
    content = StringField(max_length=500, required=True)
    create_time = DateTimeField(default=timezone.now())

    __object_name__ = 'Comment'
    meta = {
        'ordering': ['create_time'],
    }


class Post(Document):

    author = ReferenceField('users.User', reverse_delete_rule=CASCADE)
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=1024, required=True)
    tags = ListField(StringField(max_length=50))
    comments = ListField(EmbeddedDocumentField(Comment))
    page_views = IntField(default=0)
    create_time = DateTimeField(default=timezone.now())

    __object_name__ = 'Post'
    meta = {
        'ordering': ['-create_time'],
        'app_label': 'users',
        'object_name': 'User',
    }

    @classmethod
    def create_post(cls, username, title, content):
        user = User.get_by_uesrname(username)
        post = cls(user=user, title=title, content=content)
        post.save()
        return post
