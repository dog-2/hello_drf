from django.urls import path

app_name = 'api'

from django.conf.urls import url

from . import views
urlpatterns = [
    path('global_exception/', views.GlobalExceptionView.as_view()),
    path('local_exception/', views.LocalExceptionView.as_view()),
]