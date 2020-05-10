from django.urls import path

from . import views

urlpatterns = [
     path('cars/', views.CarListAPIView.as_view()),     # SearchFilter
     path('cars2/', views.CarListAPIView2.as_view()),   # OrderingFilter
     path('cars3/', views.CarListAPIView3.as_view()),   # 自定义fitler
     path('cars4/', views.CarListAPIView4.as_view()),   # 插件django-filter
]