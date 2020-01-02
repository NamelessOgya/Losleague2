
from django.contrib import admin
from django.urls import include, path
from attendance import views
urlpatterns = [
    path('', views.home),
    path('attendance/', include('attendance.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('logout/', views.logout),
    path('schedule/', views.schedule),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), #追加
    path('password_change/done/', views.PasswordChange, name='password_change_done'), #追加
]