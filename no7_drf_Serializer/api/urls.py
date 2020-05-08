from django.urls import path

app_name = 'api'

from django.conf.urls import url

from . import views
urlpatterns = [
    path('users/', views.User.as_view()),
    path('users/<int:pk>/', views.User.as_view()),
]