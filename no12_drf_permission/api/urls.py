from django.urls import path

from . import views

urlpatterns = [
    path('test3/', views.TestAdminOrReadOnlyAPIView.as_view()),
]
