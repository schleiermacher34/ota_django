from django.urls import path
from . import views

urlpatterns = [
    path('check_update/', views.check_update, name='check_update'),
]
