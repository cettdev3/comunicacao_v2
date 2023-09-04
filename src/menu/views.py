from django.shortcuts import render, redirect
from login.models import Usuarios
from django.contrib.auth.decorators import login_required

import requests
