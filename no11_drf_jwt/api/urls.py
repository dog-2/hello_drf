from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# ObtainJSONWebToken视图类就是通过username和password得到user对象然后签发token（生成token）
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token

from . import views

urlpatterns = [
    #path('jogin/', ObtainJSONWebToken.as_view()),
    path('jwt/', obtain_jwt_token),
    path('user/detail/', views.UserDetail.as_view()),
    path('simple_jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('simple_jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/detail2/', views.UserDetail2.as_view()),
]