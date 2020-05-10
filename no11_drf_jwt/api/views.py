from rest_framework.views import APIView
from utils.response import APIResponse
# 必须登录后才能访问 - 通过了认证权限组件
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserDetail(APIView):
    authentication_classes = [JSONWebTokenAuthentication]  # jwt-token校验request.user
    permission_classes = [IsAuthenticated]  # 结合权限组件筛选掉游客
    def get(self, request, *args, **kwargs):
        return APIResponse(results={'username': request.user.username})
    
class UserDetail2(APIView):
    authentication_classes = [JWTAuthentication]  # jwt-token校验request.user
    permission_classes = [IsAuthenticated]  # 结合权限组件筛选掉游客
    def get(self, request, *args, **kwargs):
        return APIResponse(results={'username': request.user.username})