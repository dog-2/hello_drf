from rest_framework.generics import ListAPIView 


from . import models, serializers


# drf的SearchFilter
# 第一步： 搜索过滤
from rest_framework.filters import SearchFilter

class CarListAPIView(ListAPIView):
    queryset = models.Car.objects.all() 
    serializer_class = serializers.CarModelSerializer  #自定义认证

    # 第二步：局部配置 过滤类 们（全局配置用DEFAULT_FILTER_BACKENDS）
    filter_backends = [SearchFilter]

    # 第三步：SearchFilter过滤类依赖的过滤条件 => 接口：/cars/?search=...
    search_fields = ['name', 'price']  #筛选字段
    # eg：/cars/?search=1，name和price中包含1的数据都会被查询出


# 第一步：drf的OrderingFilter - 排序过滤
from rest_framework.filters import OrderingFilter

class CarListAPIView2(ListAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer

    # 第二步：局部配置 过滤类 们（全局配置用DEFAULT_FILTER_BACKENDS）
    filter_backends = [OrderingFilter]

    # 第三步：OrderingFilter过滤类依赖的过滤条件 => 接口：/cars/?ordering=...
    ordering_fields = ['pk', 'price']
    # eg：/cars/?ordering=-price,pk，先按price降序，如果出现price相同，再按pk升序




# 自定义fitler
from .filters import LimitFilter

class CarListAPIView3(ListAPIView):
    # 如果queryset没有过滤条件，就必须 .all()，不然分页会出问题
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer
    
    # 局部配置 过滤类 们（全局配置用DEFAULT_FILTER_BACKENDS）
    filter_backends = [LimitFilter]
    

# django-filter插件过滤器
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CarFilterSet

class CarListAPIView4(ListAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer
    
    # 局部配置 过滤类 们（全局配置用DEFAULT_FILTER_BACKENDS）
    filter_backends = [DjangoFilterBackend]
    
    # django-filter过滤器插件使用
    #filter_class = CarFilterSet
    filterset_class = CarFilterSet  # 旧版写作filter_class, 新版写作fitlerset_class
    # 接口：?brand=...&min_price=...&max_price=...
    # eg:?brand=宝马&min_price=5&max_price=10 => 5~10间的宝马牌汽车