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

from utils.security import (
    Allow,
    Deny,
    EveryOne,
    Owner,
    Authenticated,
)
from utils.mixins import PermissionMixin
from users.models import User

class Comment(EmbeddedDocument):

    author = ReferenceField('users.User')
    content = StringField(max_length=500, required=True)
    create_time = DateTimeField(default=timezone.now())

    __object_name__ = 'Comment'
    __acl__ = [
        (Allow, EveryOne, 'view'),
        (Allow, Authenticated, 'add'),
        (Allow, Owner, 'change'),
        (Allow, Owner, 'delete'),
    ]
    meta = {
        'ordering': ['create_time'],
    }

    @classmethod
    def create_comment(cls, post_id, username, content):
        post = Post.get_by_id(post_id)
        user = User.get_by_uesrname(username)
        comment = cls(author=user, content=content)
        Post.objects(id=post_id).update_one(push__comments=comment)


class Post(PermissionMixin, Document):

    author = ReferenceField('users.User', reverse_delete_rule=CASCADE)
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=1024, required=True)
    tags = ListField(StringField(max_length=50))
    comments = ListField(EmbeddedDocumentField(Comment))
    page_views = IntField(default=0)
    create_time = DateTimeField(default=timezone.now())

    __object_name__ = 'Post'
    __acl__ = [
        (Allow, EveryOne, 'view'),
        (Allow, Authenticated, 'add'),
        (Allow, Owner, 'change'),
        (Allow, Owner, 'delete'),
    ]
    meta = {
        'ordering': ['-create_time'],
    }

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def create_post(cls, username, title, content):
        user = User.get_by_uesrname(username)
        post = cls(author=user, title=title, content=content)
        post.save()
        return post

    def is_owner(self, username):
        return self.author.username == username
