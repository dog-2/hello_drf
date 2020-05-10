from rest_framework.views import APIView

from .throttles import SMSRateThrottle
from utils.response import APIResponse

class TestSMSAPIView(APIView):
    # 局部配置频率认证
    throttle_classes = [SMSRateThrottle]
    def get(self, request, *args, **kwargs):
        return APIResponse(0, 'get 获取验证码 OK')
    def post(self, request, *args, **kwargs):
        return APIResponse(0, 'post 获取验证码  OK')