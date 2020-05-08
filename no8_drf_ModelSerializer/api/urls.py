from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('v1/books/', views.Book.as_view()),
    path('v1/books/<pk>/', views.Book.as_view()),
    path('v2/books/', views.V2Book.as_view()),
    path('v2/books/<pk>/', views.V2Book.as_view()),
]