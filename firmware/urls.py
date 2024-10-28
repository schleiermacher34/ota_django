from django.urls import path, include
from . import views

urlpatterns = [
    path('check_update/', views.check_update, name='check_update'),
    path('api/validate_license/', views.validate_license, name='validate_license'),
    path('api/upload_log/', views.upload_log, name='upload_log'),
    path('api/get_token/', views.get_token, name='get_token'),
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
    path('sync_vtiger/', views.sync_vtiger, name='sync_vtiger'),
]
