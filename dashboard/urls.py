from django.urls import path
from . import views

urlpatterns = [
    # /dashboard/
    path('', views.index, name='dashboard'),
    # eg: /dashboard/btc/
    path('<str:symbol>/', views.index, name='dashboard'),

]