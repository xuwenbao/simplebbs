Simplebbs(仿V2ex论坛)
=========


[xuwenbao](https://github.com/xuwenbao), 新浪微博: [Pythoner_左奕](http://weibo.com/xuwenbao)  
- - -


简介
---------
Simplebbs,仿照V2ex实现简单论坛.您可以点击此地址访问: [63.223.73.122](http://63.223.73.122)  
+ 采用Django 1.5
+ 数据存储采用Mongodb, ORM使用[mongoengine](http://mongoengine.org/)
+ 重写Django Class View,适用于mongoengine
+ 实现ACL配置式的权限管理
+ 前端使用Bootstrap, JQuery


Class Views([src/utils/views.py](./src/utils/views.py))
--------
+ MongoCreateView
+ MongoUpdateView
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
        (Allow, Owner, 'delete'),
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
    'users.middlewares.PermissionMiddleware',
)
```  
  
为视图函数增加一个装饰器,即可实现权限管理  
```python
from utils.security import permission_view

post_list = permission_view(PostListView.as_view(), permission='view', model=Post)
```  