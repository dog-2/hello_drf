from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# drf原生处理异常函数取别名 drf_exception_handler
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response
from rest_framework import status

from . import models
from rest_framework.views import APIView
from rest_framework.response import Response


@method_decorator(csrf_exempt, name='dispatch')
class GlobalExceptionView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.query_params)
        print(request.data)
        print(request.not_exists)  # error code
        return Response('post ok')


@method_decorator(csrf_exempt, name='dispatch')
class LocalExceptionView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.query_params)
        print(request.data)
        print(request.not_exists)  # error code
        return Response('post ok')

    def get_exception_handler(self):
        return self.exception_handler

    def exception_handler(self, exc, context):
        # drf的exception_handler做基础处理
        response = drf_exception_handler(exc, context)
        # 为空，就是drf框架处理不了的异常
        if response is None:  # 处理之后为空，再进行自定义的二次处理
            # print(exc)    #错误原因   还可以做更详细的原因，通过判断exc信息类型
            # print(context)  #错误信息
            print('%s - %s - %s' %
                  (context['view'], context['request'].method, exc))
            return Response({
                'detail': 'local customized exception: internal server error'  # 局部定制异常：服务器错误
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)
        return response  # 处理之后有值，就直接返回结果
