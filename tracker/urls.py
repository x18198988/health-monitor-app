from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_data, name='add_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),  
    path('export/', views.export_csv, name='export_csv'),
]
