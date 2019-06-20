from django.shortcuts import render, redirect
from repository import models
from backend.auth import auth


@auth.check_login
def manage_index(request):
    """
    管理界面首页
    :param request:
    :return:
    """
    context = {
        'user_info': request.session.get('user_info'),
    }
    print(request.session.get('user_info'))
    return render(request, 'backend/backend_index.html', context)


@auth.check_login
def base_info(request):
    return render(request, 'backend/backend_user_info.html')