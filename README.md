Simplebbs(仿V2ex论坛)
=========


[xuwenbao](https://github.com/xuwenbao)  
- - -


简介
---------
Simplebbs,仿照V2ex实现完整论坛功能. 
+ 使用Django 1.5
+ 数据存储使用Mongodb, ORM使用[mongoengine](http://mongoengine.org/)
+ 重写Django Class View,适用于mongoengine快速开发
+ 简单并有良好拓展性的ACL配置式的权限管理
+ 前端使用Bootstrap, JQuery


Class Views([src/utils/views.py](./src/utils/views.py))
--------
+ MongoCreateView
+ MongoUpdateView
+ MongoDeleteView
+ MongoDetailView
+ MongoListView


ACL权限管理
--------

为需要权限管理的任何类设置一个 **\_\_acl\_\_** 属性,如:  
```python
from utils.security import (
    Allow,
    Deny,
    EveryOne,
    Owner,
    Authenticated,
)

class MyDocumnet(object):
    __acl__ = [
        (Allow, EveryOne, 'view'),
        (Allow, Authenticated, 'add'),
        (Allow, Owner, 'change'),
        (Allow, 'group:admin', 'delete'),
    ]
```  
新增一个Django Middleware: [users.middlewares.PermissionMiddleware](./src/users/middlewares.py)  
```python
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    **'users.middlewares.PermissionMiddleware',**
)
```  

为视图函数增加一个装饰器,即可实现权限管理  
```python
from utils.security import permission_view

post_list = permission_view(PostListView.as_view(), permission='view', model=Post)
```  


Model Permission Mixin([PermissionMixin](./src/utils/mixins.py))
--------

使用Model类继承PermissionMixin  
```python
class Post(PermissionMixin, Document):
    pass
```  

model实例权限判断:
```python
post.has_perm(permission, user_groups, username)
```  
