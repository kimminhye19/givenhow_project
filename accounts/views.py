from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from . import forms


# 회원가입
@csrf_exempt
def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        userid = request.POST.get('userid', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        res_data = {}
        if not (userid and password and re_password):
            res_data['error'] = '모든 값을 입력하세요!'
            return render(request, 'accounts/signup.html', res_data)
        elif password != re_password:
            res_data['error'] = '비밀번호가 일치하지 않습니다!'
            return render(request, 'accounts/signup.html', res_data)
        elif Users.objects.filter(userid=userid).exists():
            res_data['error'] = '이미 사용중인 아이디입니다!'
            return render(request, 'accounts/signup.html', res_data)
        else:
            accounts = Users(userid=userid, password=make_password(password))
            accounts.save()
        return redirect('/accounts/new_login')


@csrf_exempt
def new_login(request):
    if request.method == 'GET':
        form = forms.LoginForm()
        return render(request, 'accounts/new_login.html', {'form': form})
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.userid
            return redirect('/chucheon/survey')
    else:
        form = forms.LoginForm()
    return render(request, "accounts/new_login.html", {'form': form})


@csrf_exempt
def existing_login(request):
    if request.method == 'GET':
        form = forms.LoginForm()
        return render(request, 'accounts/existing_login.html', {'form': form})
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.userid
            return redirect('/chucheon/like1')
    else:
        form = forms.LoginForm()
    return render(request, "accounts/existing_login.html", {'form': form})


# 로그아웃
@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect('/')

