from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class Book(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 单查
        if pk:
            try:
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                book_data = serializers.BookModelSerializer(
                    book_obj).data  # 单条数据序列化
            except Exception as err:
                return Response({
                    'status': 1,
                    'msg': '数据不存在'
                })
        # 群查
        else:
            book_query = models.Book.objects.filter(
                is_delete=False).all()  # 先筛选查询,再查所有
            book_data = serializers.BookModelSerializer(
                book_query, many=True).data  # 不管是一条还是多条，只要数据是被[]嵌套，都要写many=True
        # 返回前端数据
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': book_data
        })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        book_ser = serializers.BookModelDeserializer(data=request_data)
        # raise_exception=True：当校验失败，马上终止当前视图方法，抛异常返回给前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.BookModelSerializer(book_obj).data
        })


class V2Book(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        # 单查
        if pk:
            try:
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                book_data = serializers.V2BookModelSerializer(
                    book_obj).data  # 序列化
            except:
                return Response({
                    'status': 1,
                    'msg': '参数有误'
                })
        # 群查
        else:
            book_query = models.Book.objects.filter(is_delete=False).all()
            book_data = serializers.V2BookModelSerializer(
                book_query, many=True).data  # 序列化

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': book_data
        })

    def post(self, request, *args, **kwargs):
        # 单增:传的数据是与model对应的一个字典
        # 群增：设计传递的是多个model对应的字典列表,在postman中通过列表嵌套字典传值
        request_data = request.data
        if isinstance(request_data, dict):  # 判断获取的数据是否是dict
            many = False
        elif isinstance(request_data, list):  # 判断获取的数据是否是list
            many = True
        else:
            return Response({
                'status': 1,
                'msg': '数据错误'
            })
        book_ser = serializers.V2BookModelSerializer(
            data=request_data, many=many)  # 反序列化
        book_ser.is_valid(raise_exception=True)
        # book_result是对象<class 'app01.models.Book'>，群增就是列表套一个个对象
        book_result = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_result, many=many).data
        })

    # 单删: 有pk   #在postman中通过路径传参
    # 群删：有pks   {"pks": [1, 2, 3]}   #通过json传参
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')
        if models.Book.objects.filter(pk__in=pks, is_delete=False).update(is_delete=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

    # 单整体改
    def put(self, request, *args, **kwargs):
        return self._modify_one(request=request, partial=False, *args, **kwargs)

    # 单局部改
    def patch(self, request, *args, **kwargs):
        return self._modify_one(request=request, partial=True, *args, **kwargs)

    # 单改
    # partial为False则为单整体改
    # partial为True则为单局部改
    def _modify_one(self, request, partial, *args, **kwargs):
        request_data = request.data
        pk = kwargs.get('pk')
        # 先获取要修改的对象
        try:
            old_book_obj = models.Book.objects.get(pk=pk, is_delete=False)
        except:
            # 当输入不存在的pk
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        book_ser = serializers.V2BookModelSerializer(
            instance=old_book_obj, data=request_data, partial=partial)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V2BookModelSerializer(book_obj).data
        })