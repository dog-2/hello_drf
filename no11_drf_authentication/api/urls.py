from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.TestAPIView.as_view()),
]