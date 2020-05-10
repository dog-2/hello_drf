from rest_framework.views import APIView

from utils.response import APIResponse

class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 如果通过了认证组件，request.user就一定有值
        # 游客：AnonymousUser
        # 用户：User表中的具体用户对象
        print(request.user)
        return APIResponse(0, 'test get ok')