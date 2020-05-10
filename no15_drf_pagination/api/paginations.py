from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    # ?page=页码  定义代表页码的属性，如果写pages,就是?pages=页码
    page_query_param = 'page'
    # ?page=页码 设置默认下一页显示的条数
    page_size = 3
    # ?page=页码&page_size=条数 用户自定义一页显示的条数
    page_size_query_param = 'page_size'
    # 用户自定义一页显示的条数最大限制：数值超过5也只显示5条
    max_page_size = 5



from rest_framework.pagination import LimitOffsetPagination

class MyLimitOffsetPagination(LimitOffsetPagination):
    # ?offset=从头偏移的条数&limit=要显示的条数
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    # ?不传offset和limit默认显示前3条，只设置offset就是从偏移位往后再显示3条
    default_limit = 3
    # ?limit可以自定义一页显示的最大条数
    max_limit = 5

    #eg:/cars/?offset=1&limit=4  往后偏移一位，然后往后数四个数据

    # 只使用limit结合ordering可以实现排行前几或后几
    #？ordering=-price&limit=2  价格降序，取最前面两条数据
    
    
    
# 注：必须基于排序规则下进行分页
# 1）如果接口配置了OrderingFilter过滤器，那么url中必须传ordering
# 1）如果接口没有配置OrderingFilter过滤器，一定要在分页类中声明ordering按某个字段进行默认排序
from rest_framework.pagination import CursorPagination

class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
    ordering = '-pk'
