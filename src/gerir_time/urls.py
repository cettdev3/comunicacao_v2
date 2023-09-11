from django.urls import include, path
from gerir_time.views import Gerir_time


urlpatterns = [
    path('gerir-time',  Gerir_time),

]