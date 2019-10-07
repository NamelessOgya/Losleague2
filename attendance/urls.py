from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user),
    path('index/', views.index, name='index'),
    path('index/register/<str:date>/', views.date),
    path('match_list', views.listdate),
    path('<str:date>/result', views.result, name='result'),
    path('matchlist/<str:date>/', views.list),
    path('report_date/report/<str:date>/', views.report),
    path('report_date/report/<str:date>/result', views.report_register),
    path('report_date/', views.reportdate),
    path('match_result', views.match_result)

]