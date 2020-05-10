from rest_framework.views import APIView

from utils.permissions import MyPermission
from utils.response import APIResponse

# 游客只读，登录用户只读，只有登录用户属于 管理员 分组，才可以增删改
class TestAdminOrReadOnlyAPIView(APIView):
    permission_classes = [MyPermission]
    # 所有用户都可以访问
    def get(self, request, *args, **kwargs):
        return APIResponse(0, '自定义读 OK')
    # 必须是 自定义“管理员”分组 下的用户
    def post(self, request, *args, **kwargs):
        return APIResponse(0, '自定义写 OK')