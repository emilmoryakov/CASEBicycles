from django.urls import path
from .views import log_stats_view

urlpatterns = [
    path('stats/', log_stats_view, name='log_stats')
]