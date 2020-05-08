from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser   #用作解析类

@method_decorator(csrf_exempt, name='dispatch')
class Book(APIView):
    # 局部解析类配置,post提交数据只能解析json格式数据
    parser_classes = [      # 如果[]为空，那么就相当于没有设置解析类型
        JSONParser,         # json数据包
        # FormParser,       # x-www-form-urlencoded数据包
        # MultiPartParser,  # form-data数据包
    ]
    def post(self, request, *args, **kwargs):
        # url拼接参数：只有一种传参方式就是拼接参数
        print(request.query_params)
        # 数据包参数：有三种传参方式，form-data、urlencoding、json
        print(request.data)
        return Response('post ok')
