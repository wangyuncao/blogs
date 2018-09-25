from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from backweb.models import User


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 得到当前地址
        path = request.path
        flag = ['/backweb/my_login/', '/backweb/my_register/']

        if ('front' in path) or (path in flag):
            # 如果地址是不用登录的地址，放弃判断
            return None

        # 得到本地COOKIES的值
        session_id = request.COOKIES.get('session_id')
        if not session_id:
            # 本地cookie中没有sesson_id值，说明用户根本没有登录
            return HttpResponseRedirect(reverse('backweb:my_login'))

        user = User.objects.filter(session_id=session_id).first()
        if not user:
            # 用户不存在，说明session_id不正确
            return HttpResponseRedirect(reverse('backweb:my_login'))

        user_permission = [p.p_name for p in user.u_r.r_p.all()]
        user.user_permission = user_permission

        # 把用户传给页面
        request.user = user
        # 不返回就可以
        return None