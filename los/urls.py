
from django.contrib import admin
from django.urls import include, path
from attendance import views
urlpatterns = [
    path('', views.home, name="home"),
    path('attendance/', include('attendance.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('logout/', views.logout),
    path('schedule/', views.schedule),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), #追加
    path('password_change/done/', views.PasswordChange, name='password_change_done'), #追加
    path('user/', views.user,name='user'),
    path('team_page/<str:team_name>/',views.team_page),
    path("jcgrank", views.jcgrank),
    path('team_page',views.team_page_home)
]