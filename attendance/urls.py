from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user),
    path('index/', views.index, name='index'),
    path('index/register/<str:date>/', views.date),
    path('match_list', views.listdate),
    path('<str:date>/result', views.result, name='result'),
    path('matchlist/<str:date>/', views.listmake),
    path('matchlistsu/<str:date>/', views.listsu),
    path('report_date/report/<str:date>/', views.report),
    path('report_date/report/<str:date>/result', views.report_register),
    path('report_date/', views.reportdate),
    path('match_result', views.match_result),
    path('check', views.check),
    path('update', views.update),
    path('update2', views.update2),
    path('update3', views.update3),
    path('final', views.final),
    path('past', views.past),
    path('member', views.member),
    path('release_changed/<str:date>', views.release_changed),
    path('team_page_edit', views.team_page_edit),
    path('team_page_edit/done', views.team_page_edit_done),
]