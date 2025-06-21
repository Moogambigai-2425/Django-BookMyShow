from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     path('', user_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
