from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import models
from . import serializers
from .response import APIResponse


class BookGenericAPIView(GenericAPIView):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer
    lookup_field = 'pk'  # 先定义好，单查可以使用，默认是pk  自定义主键的有名分组，如果路由有名分组不是pk,这个属性就要自己设置了
   
    # 群取
    def get(self, request, *args, **kwargs):
        book_query = self.get_queryset()  # 获取queryset数据（model查询数据）
        book_ser = self.get_serializer(book_query, many=True)
        book_data = book_ser.data
        return APIResponse(results=book_data)

    # # 单取
    # def get(self, request, *args, **kwargs):
    #     book_query = self.get_object()
    #     book_ser = self.get_serializer(book_query)
    #     book_data = book_ser.data
    #     return APIResponse(results=book_data)


class BookMixinGenericAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    # GenericAPIView提供的序列化器和查询的数据
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    # 单查和群查
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            # 单查  RetrieveModelMixin方法
            response = self.retrieve(request, *args, **kwargs)
        else:
            # mixins提供的list方法的响应对象是Response，将该对象格式化为自定义的APIResponse
            response = self.list(request, *args, **kwargs)  # 群查 ListModelMixin
        # response的数据都存放在response.data中
        return APIResponse(results=response.data)

    # 单增
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)  # CreateModelMixin方法
        return APIResponse(results=response.data)

    # 单整体修改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)  # UpdateModelMixin
        return APIResponse(results=response.data)

    # 单局部修改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)


class BookListCreatePIView(ListCreateAPIView, UpdateAPIView):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer


class BookGenericViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    def my_get_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def my_get_obj(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BookModelViewSet(ModelViewSet):
    queryset = models.Book.objects.filter(is_delete=False)
    serializer_class = serializers.BookModelSerializer

    # 删不是数据库，而是该记录中的修改is_delete的值，因此重写默认的destroy函数
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # type: models.Book
        if not instance:
            return APIResponse(1, '删除失败')  # 实际操作，在此之前就做了判断
        instance.is_delete = True
        instance.save()
        return APIResponse(0, '删除成功')
