from django.urls import include, path
from login.views import login_page,Autenticar
from django.contrib.auth import views as auth_views
from login.views import Logout_Users
urlpatterns = [
    path('',  login_page),
    path('dologin', Autenticar ),
    path('logout', Logout_Users, name='Logout'),

]