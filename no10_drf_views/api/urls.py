from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'


router = SimpleRouter()
# 所有路由与ViewSet视图类的都可以注册，会产生 '^v6/books/$' 和 '^v6/books/(?P<pk>[^/.]+)/$'
router.register('v7/books', views.BookModelViewSet)

urlpatterns = [
    path('v2/books/', views.BookGenericAPIView.as_view()),
    path('v2/books/<pk>/', views.BookGenericAPIView.as_view()),
    path('v3/books/', views.BookMixinGenericAPIView.as_view()),
    path('v3/books/<pk>/', views.BookMixinGenericAPIView.as_view()),
    path('v4/books/', views.BookListCreatePIView.as_view()),
    path('v4/books/<pk>/', views.BookListCreatePIView.as_view()),
    path('v5/books/',
         views.BookGenericViewSet.as_view({'get': 'my_get_list'})),
    path('v5/books/<pk>/',
         views.BookGenericViewSet.as_view({'get': 'my_get_obj'})),
    path('v6/books/',
         views.BookModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('v6/books/<pk>/', views.BookModelViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    
    # router.urls添加方法一
    # path('', include(router.urls)),
]



# router.urls添加方法二
urlpatterns += router.urls

