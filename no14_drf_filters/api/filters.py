from . import models

# 自定义过滤器，接口：?limit=显示的条数
class LimitFilter:
    def filter_queryset(self, request, queryset, view):
        # 前台固定用 ?limit=... 传递过滤参数
        limit = request.query_params.get('limit')
        if limit:
            limit = int(limit)
            return queryset[:limit]
        return queryset
    

# django-fitler插件：自定义过滤字段
from django_filters import filters
from django_filters.rest_framework.filterset import FilterSet

class CarFilterSet(FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    class Meta:
        model = models.Car
        fields = ['brand', 'min_price', 'max_price']
        # brand是model中存在的字段，一般都是可以用于分组的字段
        # min_price、max_price是自定义字段，需要自己自定义过滤条件