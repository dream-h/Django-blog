#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from io import BytesIO
from utils.check_code import create_validate_code
from django.shortcuts import render, redirect, HttpResponse
from web.forms.account import LoginForm, RegisterForm
from repository.models import UserInfo


def check_code(request):
    """
    验证码图片生成并返回
    :param request:
    :return:
    """
    steam = BytesIO()
    img, code = create_validate_code()
    img.save(steam, 'PNG')
    request.session['check_code'] = code
    return HttpResponse(steam.getvalue())


def login(request):
    """
    登录函数
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'web_home/login.html')
    elif request.method == 'POST':
        result = {
            'status': False, 'message': None, 'data': None
        }
        login_form = LoginForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user_info = UserInfo.objects.filter(username=username, password=password)\
                .values(
                'nid', 'nickname', 'username', 'email',
                'avatar', 'blog__nid', 'blog__site'
            ).first()
            if not user_info:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
                if login_form.cleaned_data.get('rmeb') == True:
                    request.session.set_expiry(60*60*24*30)
        else:
            print(login_form.errors)
            if 'check_code' in login_form.errors:
                result['message'] = '验证码错误'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))


def logout(request):
    """
    用户退出函数
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/')


def register(request):
    """
    用户注册函数
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'web_home/register.html')
    else:
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_info_data = register_form.cleaned_data
            print(user_info_data)
            username = user_info_data.get('username')
            nickname = user_info_data.get('nickname')
            email = user_info_data.get('email')
            password = user_info_data.get('password')
            user_info = UserInfo.objects.create(
                username=username, password=password, nickname=nickname,
                email=email, avatar='avatar/4bf842cdf17b2034b8b2a447e3081ec3.jpg'
            )
            #request.session['user_info'] = json.dump(user_info)
            return redirect('web:home')
        else:
            print(register_form.errors)
            context = {
                'register_form': register_form,
            }
            return render(request, 'web_home/register.html', context)

