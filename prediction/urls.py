from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('result/<int:prediction_id>/', views.result, name='result'),
    path('health/', views.health_check, name='health_check'),
]