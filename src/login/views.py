from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.middleware.csrf import get_token
from django.http import HttpResponse

def decrypt(ciphertext, key):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher = "".join(key)
    plaintext = ""

    for char in ciphertext:
        if char.isalpha():
            idx = alphabet.index(char)
            new_char = cipher[idx] if char.isupper() else cipher[idx]
            plaintext += new_char
        else:
            plaintext += char

    return plaintext

@csrf_exempt 
def login_page(request):
    if request.GET:
        try:
            dados = str(request.GET['hash'])
            dados = dados.split('-')
            usuario = decrypt(dados[0],'azbycxdwevfugthsirjqkplomnAZBYCXDWEVFUGTHSIRJQKPLOMN')
            senha = decrypt(dados[1],'azbycxdwevfugthsirjqkplomnAZBYCXDWEVFUGTHSIRJQKPLOMN')
            dados = {'usuario':usuario,'senha':senha}

            return render(request, 'login.html',{'dados':dados})
        
        except:
             return render(request, 'login.html',{'usuario':'','senha':''})
    else:
        return render(request, 'login.html',{'usuario':'','senha':''})

def Logout_Users(request):
    logout(request)
    return redirect('/')

@csrf_protect
def Autenticar(request):
    #return render(request,"forms.html")
    if request.POST:
        username = request.POST['usuario']
        password = request.POST['senha']
            

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/solicitacoes')
        else:
            messages.error(request, ' Usuário/Senha inválidos!')
            return redirect('/')