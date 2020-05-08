from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('v3/books/', views.V3Book.as_view()),
    path('v3/books/<pk>/', views.V3Book.as_view()),
]