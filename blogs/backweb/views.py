from datetime import datetime, timedelta

from django.contrib import auth
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from backweb.models import Article, Atype, User, Role, Permission

import random


def login(request):
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户名和密码是否正确
        # 用auth_user数据库的匹配输入信息
        user = auth.authenticate(request,
                          username=username,
                          password=password)
        # 验证用户成功
        if user:
            # 登录
            auth.login(request, user)
            return HttpResponseRedirect(reverse('backweb:index'))
        else:
            return HttpResponseRedirect(reverse('backweb:login'))


def index(request):
    if request.method == 'GET':
        return render(request, 'backweb/index.html')


def logout(request):
    if request.method == 'GET':
        # 退出
        auth.logout(request)
        return HttpResponseRedirect(reverse('backweb:login'))


def management(request):
    if request.method == 'GET':
        # 使用切片实现分页
        # 第一种
        # page_num = request.GET.get('page', 1)
        # start_art = 1 * (int(page_num) - 1)
        # end_art = 1 * (int(page_num))
        # arts = Article.objects.all()[start_art: end_art]
        # 第二种
        # 如果没值就给page赋1
        judge = request.GET.get('judge', '')
        price = request.GET.get('price', '')
        if judge == 'a_name':
            articles = Article.objects.filter(Q(a_name__contains=price) | Q(a_content__contains=price))
        elif judge == 'id':
            articles = Article.objects.filter(id=price)
        else:
            articles = Article.objects.all()

        page_num = int(request.GET.get('page', 1))
        # Paginator给对象分页
        paginator = Paginator(articles, 5)
        arts = paginator.page(page_num)
        return render(request, 'backweb/management.html', {'arts': arts,
                                                           'judge': judge,
                                                           'price': price})
    if request.method == 'POST':
        judge = request.POST.get('judge')
        price = request.POST.get('price')
        if judge == 'a_name':
            articles = Article.objects.filter(a_name__contains=price)
        else:
            articles = Article.objects.filter(id=int(price))
        page_num = int(request.GET.get('page', 1))
        # Paginator给对象分页
        paginator = Paginator(articles, 5)
        arts = paginator.page(page_num)
        return render(request, 'backweb/management.html', {'arts': arts})


def daaman(request):
    if request.method == 'GET':
        types = Atype.objects.all()
        return render(request, 'backweb/daaman.html', {'types': types})
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        content = request.POST.get('content')
        img = request.FILES.get('img')
        a_conceal = request.POST.get('a_conceal')
        a_recommend = request.POST.get('a_recommend')
        a_conceal = True if a_conceal == 'on' else False
        a_recommend = True if a_recommend == 'on' else False

        Article.objects.create(a_name=name,
                               a_desc=desc,
                               a_category_id=int(category),
                               a_content=content,
                               a_conceal=a_conceal,
                               a_recommend=a_recommend,
                               image_url=img)
        return HttpResponseRedirect(reverse('backweb:management'))


def password(request):
    if request.method == 'GET':
        return render(request, 'backweb/password.html')
    if request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        session_id = request.COOKIES.get('session_id')
        user = User.objects.filter(session_id=session_id)
        if user[0].password != oldpassword:
            return render(request, 'backweb/password.html', {'error': '旧密码不正确'})
        if password1 != password2:
            return render(request, 'backweb/password.html', {'error': '两次密码不正确'})
        user.update(password=password2)
        return render(request, 'backweb/login.html', {'error': '密码修改成功，请重新登录'})


def conceal(request, id):
    if request.method == 'GET':
        arts = Article.objects.filter(id=id)
        flag = arts[0].a_conceal
        if flag:
            arts.update(a_conceal=False)
        else:
            arts.update(a_conceal=True)
        return HttpResponseRedirect(reverse('backweb:management'))


def recommend(request, id):
    if request.method == 'GET':
        arts = Article.objects.filter(id=id)
        flag = arts[0].a_recommend
        if flag:
            arts.update(a_recommend=False)
        else:
            arts.update(a_recommend=True)
        return HttpResponseRedirect(reverse('backweb:management'))


def delman(request, id):
    if request.method == 'GET':
        Article.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('backweb:management'))


def updateman(request, id):
    if request.method == 'GET':
        artdd = Article.objects.get(id=id)
        types = Atype.objects.all()
        return render(request, 'backweb/updateman.html', {'artdd': artdd, 'types': types, 'id1': id})
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        content = request.POST.get('content')
        img = request.FILES.get('img')

        Article.objects.filter(id=id).update(a_name=name,
                                             a_desc=desc,
                                             a_category_id=category,
                                             a_content=content)
        if img:
            Article.objects.filter(id=id).update(image_url=img)
        return HttpResponseRedirect(reverse('backweb:management'))


def my_register(request):
    if request.method == 'GET':
        return render(request, 'backweb/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 先验证用户是否注册过
        user = User.objects.filter(username=username).exists()
        if user:
            error = '用户名已经存在，请直接登录'
            return render(request, 'backweb/register.html', {'error': error})
        else:
            # 两次密码正确
            if password1 == password2:
                User.objects.create(username=username, password=password1)
                return HttpResponseRedirect(reverse('backweb:my_login'))
            else:
                error = '两次密码不正确'
                return render(request, 'backweb/register.html', {'error': error})


def my_login(request):
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username, password=password).first()
        if user:
            # 帐号密码正确
            # 第一步，给地址的cookie设值
            res = HttpResponseRedirect(reverse('backweb:index'))
            s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
            session_id = ''
            for i in range(20):
                session_id += random.choice(s)
            out_time = datetime.now() + timedelta(days=1)
            res.set_cookie('session_id', session_id, expires=out_time)
            # 第二步，服务端存cookie中设的值
            user.session_id = session_id
            user.out_time = out_time
            user.save()
            # 返回地址
            return res
        else:
            error = '用户名或密码错误'
            return render(request, 'backweb/login.html', {'error': error})


def my_logout(request):
    if request.method == 'GET':
        # 1.删除服务端的session_id值
        user = request.user
        user.session_id = ''
        user.save()
        # 2.删除浏览器的session_id值
        res = HttpResponseRedirect(reverse('backweb:index'))
        res.delete_cookie('session_id')
        return res


def add_user(request):
    if request.method == 'GET':
        return render(request, 'backweb/add_user.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.filter(username=username).exists()
        if user:
            error = '员工账号已存在'
            return render(request, 'backweb/add_user.html', {'error': error})
        if password1 == password2:
            User.objects.create(username=username, password=password1)
            # 创建用户成功返回用户列表
            return HttpResponseRedirect(reverse('backweb:list_user'))
        else:
            error = '两次输入密码不正确'
            return render(request, 'backweb/add_user.html', {'error': error})


def list_user(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'backweb/list_user.html', {'users': users})


def role_premission(request):
    if request.method == 'GET':
        # 角色列表,role.r_name
        roles = Role.objects.all()
        # 权限列表,pers.p_name
        pers = Permission.objects.all()
        return render(request, 'backweb/role_premission.html', {'pers': pers, 'roles': roles})
    if request.method == 'POST':
        role_name = request.POST.get('r_name')
        pers = request.POST.getlist('pers')
        role = Role.objects.create(r_name=role_name)
        for per in pers:
            p = Permission.objects.filter(p_name=per).first()
            # 添加关系.连接名
            role.r_p.add(p)
            error = '创建成功'
        return HttpResponseRedirect(reverse('backweb:role_premission'))


def user_role(request):
    if request.method == 'GET':
        # 角色列表,role.r_name
        roles = Role.objects.all()
        # 用户列表,user.username
        users = User.objects.all()
        return render(request, 'backweb/user_role.html',
                      {'roles': roles, 'users': users})
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        u = User.objects.filter(id=user_id)
        u.update(u_r_id=role_id)
        return HttpResponseRedirect(reverse('backweb:user_role'))