from rest_framework.generics import ListAPIView

from . import models, serializers, paginations

# 基础分页 PageNumberPagination
class CarListAPIView(ListAPIView):
    # 如果queryset没有过滤条件，就必须 .all()，不然分页会出问题
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer
    
    # 分页组件 - 给视图类配置分页类即可 - 分页类需要自定义，继承drf提供的分页类即可
    pagination_class = paginations.MyPageNumberPagination

    #eg:/cars/  显示第一页三条
    #/cars/?page=2&page_size=4   每页显示4条，显示第二页的4条

# 偏移分页 LimitOffsetPagination
class CarListAPIView1(ListAPIView):
    # 如果queryset没有过滤条件，就必须 .all()，不然分页会出问题
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer
    
    # 分页组件 - 给视图类配置分页类即可 - 分页类需要自定义，继承drf提供的分页类即可
    pagination_class = paginations.MyLimitOffsetPagination
    
# 游标分页 CursorPagination
class CarListAPIView2(ListAPIView):
    # 如果queryset没有过滤条件，就必须 .all()，不然分页会出问题
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarModelSerializer
    
    # 分页组件 - 给视图类配置分页类即可 - 分页类需要自定义，继承drf提供的分页类即可
    pagination_class = paginations.MyCursorPagination