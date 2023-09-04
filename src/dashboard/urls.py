from django.urls import include, path
from dashboard.views import Dashboard

urlpatterns = [
    path('dashboard',  Dashboard)
]