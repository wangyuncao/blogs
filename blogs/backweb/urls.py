
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from backweb import views


urlpatterns = [
    # django自带登录注销
    # login_required
    # url(r'^login/', views.login, name='login'),
    # url(r'^logout/', views.logout, name='logout'),

    # 自己实现登录注册注销
    url(r'^my_register/', views.my_register, name='my_register'),
    url(r'^my_login/', views.my_login, name='my_login'),
    url(r'^my_logout/', views.my_logout, name='my_logout'),

    url(r'^index/', views.index, name='index'),
    url(r'^management/', views.management, name='management'),
    url(r'^daaman/', views.daaman, name='daaman'),
    url(r'^password/', views.password, name='password'),
    url(r'^conceal/(\d+)/', views.conceal, name='conceal'),
    url(r'^recommend/(\d+)/', views.recommend, name='recommend'),
    url(r'^delman/(\d+)/', views.delman, name='delman'),
    url(r'^updateman/(\d+)/', views.updateman, name='updateman'),

    url(r'^add_user', views.add_user, name='add_user'),
    url(r'^role_premission', views.role_premission, name='role_premission'),
    url(r'^user_role', views.user_role, name='user_role'),
    url(r'^list_user', views.list_user, name='list_user'),
]