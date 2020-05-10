# 1）继承BaseAuthentication类
# 2）重写authenticate(self, request)方法，自定义认证规则
# 3）自定义认证规则基于的条件：
#       没有认证信息返回None(游客)
#       有认证信息认证失败抛异常(非法用户)
#       有认证信息认证成功返回用户与认证信息元组(合法用户)
# 4）完全视图类的全局(settings文件中)或局部(确切的视图类)配置

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed  # 异常接收
from api import models

# 继承BaseAuthentication


class MyAuthentication(BaseAuthentication):
    """
        同前台请求头拿认证信息auth（获取认证的字段要与前台约定）
        没有auth是游客，返回None
        有auth进行校验
            失败是非法用户，抛出异常
            成功是合法用户，返回 (用户, 认证信息)
    """

    def authenticate(self, request):  # 重写authenticate方法
        # 前台在请求头携带认证信息，
        # 且默认规范用 Authorization 字段携带认证信息，
        # 后台固定在请求对象的META字段中 HTTP_AUTHORIZATION 获取
        # 认证信息auth
        auth = request.META.get('HTTP_AUTHORIZATION', None)  # 处理游客
        if auth is None:
            return None
        # 设置认证字段小规则(两段式):"auth 认证字符串" 在BasicAuthentication类中有规则范式
        auth_list = auth.split()  # 校验是否还是非法用户,不是两段，第一段不是auth就是非法用户
        if not (len(auth_list) == 2 and auth_list[0].lower() == 'auth'):
            raise AuthenticationFailed('认证信息有误，非法用户')  # 抛异常

        # 校验认证信息第二段从auth_list[1]中解析出来
        # 注：假设一种情况，信息为abc.123.xyz，就可以解析出admin用户；实际开发，该逻辑一定是校验用户的正常逻辑
        if auth_list[1] != 'abc.123.xyz':  # 校验失败
            raise AuthenticationFailed('信息错误，非法用户')

        # 最后再去数据库校验是否有此用户
        user = models.User.objects.filter(username='admin').first()
        if not user:
            raise AuthenticationFailed('用户数据有误，非法用户')

        return (user, None)
