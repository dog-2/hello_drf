from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from . import models

@method_decorator(csrf_exempt, name='dispatch')
class Book(View):
    # 查询
    def get(self, request, *args, **kwargs):
        # print(args)  #无名参数是元组
        print(kwargs)  # 有名分组是字典
        pk = kwargs.get('pk')
        if not pk:  # 群查
            # 操作数据库查询
            book_obj_list = models.Book.objects.all()
            # print(book_obj_list)
            # 序列化数据(把每条数据放在一个字典中，把所有字典数据放在一个list中,数据更好看)
            book_list = []
            for obj in book_obj_list:
                dic = {}
                dic['title'] = obj.title
                dic['price'] = obj.price
                book_list.append(dic)
            # 响应数据（后台返回给前台的数据）
            return JsonResponse({
                'status': 0,
                'msg': 'ok',
                'results': book_list
            }, json_dumps_params={'ensure_ascii': False})  # 取消中文转义
        else:  # 单查
            book_dic = models.Book.objects.filter(
                pk=pk).filter().values('title', 'price').first()
            # 如果不写first()，还是queryset对象  <QuerySet [{'title': '气球', 'price': Decimal('555.00')}]>
            # print(book_dic)  # {'title': '气球', 'price': Decimal('555.00')}
            if book_dic:
                return JsonResponse({
                    'status': 0,
                    'msg': 'ok',
                    'results': book_dic
                }, json_dumps_params={'ensure_ascii': False})  # 取消中文转义
            # 没有查询到数据
            return JsonResponse({
                'status': 1,
                'msg': '没有查询到结果',
            }, json_dumps_params={'ensure_ascii': False})  # 取消中文转义

    # 增加
    def post(self, request, *args, **kwargs):
        # print(request.POST.dict())  #{'title': '西游记', 'price': '4.55'}
        try:
            book_obj = models.Book.objects.create(
                **request.POST.dict())  # create增加数据
            if book_obj:
                return JsonResponse({
                    'status': 0,
                    'msg': 'ok',
                    'results': {'title': book_obj.title, 'price': book_obj.price}
                }, json_dumps_params={'ensure_ascii': False})
        except:
            return JsonResponse({
                'status': 1,
                'msg': '参数错误',
            }, json_dumps_params={'ensure_ascii': False})

        return JsonResponse({
            'status': 1,
            'msg': '增加错误',
        }, json_dumps_params={'ensure_ascii': False})
