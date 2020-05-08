from django.urls import path

app_name = 'api'

from django.conf.urls import url

from . import views
urlpatterns = [
    path('books/', views.Book.as_view()),
    path('books/<int:pk>/', views.Book.as_view()),
]