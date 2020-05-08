from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class V3Book(APIView):
    # 单局部改和群局部改整合
    # 单局部改：对 v3/books/pk/   pk通过路由传参，修改数据选择传参，通过数据包json传递
    # 群局部修改：v3/books/ 修改数据通过数据包传递，设置成列表格式  [{pk:1,name:123},{pk:3,price:7},{pk:7,publish:2}]
    def patch(self, request, *args, **kwargs):
        request_data = request.data  # 数据包数据
        pk = kwargs.get('pk')
        # 将单改，群改的数据都格式化成 pks=[要需要的对象主键标识] | request_data=[每个要修改的对象对应的修改数据]
        if pk and isinstance(request_data, dict):  # 单改
            pks = [pk, ]
            request_data = [request_data, ]
        elif not pk and isinstance(request_data, list):  # 群改
            pks = []
            # 遍历前台数据[{pk:1, name:123}, {pk:3, price:7}, {pk:7, publish:2}]，拿一个个字典
            for dic in request_data:
                pk = dic.pop('pk', None)  # 返回pk值
                if pk:
                    pks.append(pk)
                # pk没有传值
                else:
                    return Response({
                        'status': 1,
                        'msg': '参数错误'
                    })
        else:
            return Response({
                'status': 1,
                'msg': '参数错误'
            })
        # pks与request_data数据筛选，
        # 1）将pks中的没有对应数据的pk与数据已删除的pk移除，request_data对应索引位上的数据也移除
        # 2）将合理的pks转换为 objs
        objs = []
        new_request_data = []
        for index, pk in enumerate(pks):
            try:
                # 将pk合理的对象数据保存下来
                book_obj = models.Book.objects.get(pk=pk, is_delete=False)
                objs.append(book_obj)
                # 对应索引的数据也保存下来
                new_request_data.append(request_data[index])
            except:
                # 重点：反面教程 - pk对应的数据有误，将对应索引的data中request_data中移除
                # 在for循环中不要使用删除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        # 生成一个serializer对象
        book_ser = serializers.V3BookModelSerializer(
            instance=objs, data=new_request_data, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_objs = book_ser.save()

        return Response({
            'status': 0,
            'msg': 'ok',
            'results': serializers.V3BookModelSerializer(book_objs, many=True).data
        })
