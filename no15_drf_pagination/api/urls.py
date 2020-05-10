from django.urls import path

from . import views

urlpatterns = [
     path('cars/', views.CarListAPIView.as_view()),     # 基础分页
     path('cars1/', views.CarListAPIView1.as_view()),     # 偏移分页
     path('cars2/', views.CarListAPIView2.as_view()),   # 游标分页
]