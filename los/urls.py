
from django.contrib import admin
from django.urls import include, path
from attendance import views

urlpatterns = [
    path('', views.home),
    path('attendance/', include('attendance.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('logout/', views.logout)

]