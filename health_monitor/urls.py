from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', lambda request: redirect('dashboard')),  
]
