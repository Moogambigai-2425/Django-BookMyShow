from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users import views as user_views
urlpatterns = [
     path('', user_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),
    
]
