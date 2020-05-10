from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        # 只读接口判断
        r1 = request.method in ('GET', 'HEAD', 'OPTIONS')
        # group为有权限的分组
        group = Group.objects.filter(name='管理员').first()
        # groups为当前用户所属的所有分组
        groups = request.user.groups.all()
        r2 = group and groups # group和groups必须有值
        r3 = group in groups
        # 读接口大家都有权限，写接口必须为指定分组下的登陆用户
        return r1 or (r2 and r3)